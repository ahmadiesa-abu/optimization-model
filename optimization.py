import os
import time


class GenericValues:
    def __init__(self, capacity_storage, capacity_distribution,
                 capacity_disassembly, returning_goal, uncertain_demand,
                 penalty_excess, initial_inventory, demand, final_inventory,
                 inventory_cost, defective_percentage, labor_cost, up_bound,
                 bound):
        self.capacity_storage = capacity_storage
        self.capacity_distribution = capacity_distribution
        self.capacity_disassembly = capacity_disassembly
        self.returning_goal = returning_goal
        self.uncertain_demand = uncertain_demand
        self.penalty_excess = penalty_excess
        self.initial_inventory = initial_inventory
        self.demand = demand
        self.final_inventory = final_inventory
        self.inventory_cost = inventory_cost
        self.defective_percentage = defective_percentage
        self.labor_cost = labor_cost
        self.up_bound = up_bound
        self.bound = bound


class StorageCenter:

    def __init__(self, transp_storage_cost, distance_storage, storage_selected
                 ):
        self.transp_storage_cost = transp_storage_cost
        self.distance_storage = distance_storage
        self.storage_selected = storage_selected


class DistributionCenter:

    def __init__(self, transp_distribution_cost, distance_distribution,
                 distribution_selected):
        self.transp_distribution_cost = transp_distribution_cost
        self.distance_distribution = distance_distribution
        self.distribution_selected = distribution_selected


class DisassemblyCenter:

    def __init__(self, transp_disassembly_cost, distance_disassembly,
                 disassembly_selected):
        self.transp_disassembly_cost = transp_disassembly_cost
        self.distance_disassembly = distance_disassembly
        self.disassembly_selected = disassembly_selected


class ManufactureMethod:

    def __init__(self, hours_raw, pollution_manufacturing, manufacture_selected
                 ):
        self.hours_raw = hours_raw
        self.pollution_manufacturing = pollution_manufacturing
        self.manufacture_selected = manufacture_selected


class RefurbishmentMethod:

    def __init__(self, variable_refurbished_cost, refurbish_method_capacity,
                 order_refurbish_cost):
        self.variable_refurbished_cost = variable_refurbished_cost
        self.refurbish_method_capacity = refurbish_method_capacity
        self.order_refurbish_cost = order_refurbish_cost


class RedesignMethod:

    def __init__(self, variable_redesigned_cost, redesign_method_capacity,
                 order_redesign_cost):
        self.variable_redesigned_cost = variable_redesigned_cost
        self.redesign_method_capacity = redesign_method_capacity
        self.order_redesign_cost = order_redesign_cost


class RawSupplier:

    def __init__(self, variable_raw_cost, order_raw_cost, product_model,
                 portion_raw, supplier_selected):
        self.variable_raw_cost = variable_raw_cost
        self.order_raw_cost = order_raw_cost
        self.product_model = product_model
        self.portion_raw = portion_raw
        self.supplier_selected = supplier_selected


class ProductModel:

    def __init__(self, market_price, assembly_cost, shipping_storage_cost,
                 shipping_distribution_cost, manufacture_raw_cost,
                 market_price_refurb, shipping_disassembly_cost,
                 hours_refurbished, manufacture_refurbished_cost,
                 market_price_redesign, hours_redesigned,
                 pollution_shipping_dissasembly, pollution_shipping_storage,
                 pollution_refuribshed, pollution_dissasembly,
                 pollution_shipping_distribution, storage_centers=[],
                 distribution_centers=[], disassembly_centers=[],
                 manufacture_methods=[], refurb_methods=[],
                 redesign_methods=[]):
        self.market_price = market_price
        self.assembly_cost = assembly_cost
        self.shipping_storage_cost = shipping_storage_cost
        self.shipping_distribution_cost = shipping_distribution_cost
        self.manufacture_raw_cost = manufacture_raw_cost
        self.market_price_refurb = market_price_refurb
        self.shipping_disassembly_cost = shipping_disassembly_cost
        self.hours_refurbished = hours_refurbished
        self.manufacture_refurbished_cost = manufacture_refurbished_cost
        self.market_price_redesign = market_price_redesign
        self.hours_redesigned = hours_redesigned
        self.pollution_shipping_dissasembly = pollution_shipping_dissasembly
        self.pollution_shipping_storage = pollution_shipping_storage
        self.pollution_refuribshed = pollution_refuribshed
        self.pollution_dissasembly = pollution_dissasembly
        self.pollution_shipping_distribution = pollution_shipping_distribution
        self.storage_centers = storage_centers
        self.distribution_centers = distribution_centers
        self.disassembly_centers = disassembly_centers
        self.manufacture_methods = manufacture_methods
        self.refurb_methods = refurb_methods
        self.redesign_methods = redesign_methods


def get_sum_of_storage_centers(shipping_storage_cost, storage_centers):
    sum_of_storage_centers = 0
    for y in storage_centers:
        sum_of_storage_centers = sum_of_storage_centers + \
                                 ((shipping_storage_cost +
                                   y.transp_storage_cost * y.distance_storage)
                                  * y.storage_selected)
    return sum_of_storage_centers


def get_sum_of_distribution_centers(shipping_distribution_cost,
                                    distribution_centers):
    sum_of_distribution_centers = 0
    for y in distribution_centers:
        sum_of_distribution_centers = sum_of_distribution_centers + \
                                      ((shipping_distribution_cost +
                                        y.transp_distribution_cost
                                        * y.distance_distribution)
                                       * y.distribution_selected)
    return sum_of_distribution_centers


def get_sum_of_manufacture_method(manufacture_methods, labor_cost):
    sum_of_manufacture_method = 0
    for y in manufacture_methods:
        sum_of_manufacture_method = sum_of_manufacture_method + \
                                    (y.hours_raw * labor_cost *
                                     y.manufacture_selected)
    return sum_of_manufacture_method


def get_sum_of_products(models, generic_vals, variable_raw_cost):
    sum_of_product = 0
    for i in models:
        sum_of_storage_centers = \
            get_sum_of_storage_centers(i.shipping_storage_cost,
                                       i.storage_centers)
        sum_of_distribution_centers = \
            get_sum_of_distribution_centers(i.shipping_distribution_cost,
                                            i.distribution_centers)
        sum_of_manufacture_method = \
            get_sum_of_manufacture_method(i.manufacture_methods,
                                          generic_vals.labor_cost)

        sum_of_product = sum_of_product + (i.market_price - i.assembly_cost -
                                           sum_of_storage_centers -
                                           sum_of_distribution_centers -
                                           sum_of_manufacture_method -
                                           i.manufacture_raw_cost -
                                           variable_raw_cost)
    return sum_of_product


if __name__ == '__main__':
    indecies = [Index(), Index(), Index()]

    models = [ProductModel(), ProductModel(), ProductModel()]

    generic_vals = GenericValues()

    variable_raw_cost = 0  # value from raw_supplier loop
    sum_of_products = get_sum_of_products(models, generic_vals,
                                          variable_raw_cost)
