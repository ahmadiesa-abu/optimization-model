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
                 order_refurbish_cost, product_models= [],
                 refurbishment_selected, portion_refurb):
        self.variable_refurbished_cost = variable_refurbished_cost
        self.refurbish_method_capacity = refurbish_method_capacity
        self.order_refurbish_cost = order_refurbish_cost
        self.product_models = product_models
        self.refurbishment_selected = refurbishment_selected
        self.portion_refurb = portion_refurb


class RedesignMethod:

    def __init__(self, variable_redesigned_cost, redesign_method_capacity,
                 order_redesign_cost, product_models= [], redesign_selected,
                 portion_redesign):
        self.variable_redesigned_cost = variable_redesigned_cost
        self.redesign_method_capacity = redesign_method_capacity
        self.order_redesign_cost = order_redesign_cost
        self.product_models = product_models
        self.redesign_selected = redesign_selected
        self.portion_redesign = portion_redesign



class RawSupplier:

    def __init__(self, variable_raw_cost, order_raw_cost, product_models = [],
                 portion_raw, supplier_selected):
        self.variable_raw_cost = variable_raw_cost
        self.order_raw_cost = order_raw_cost
        self.product_models = product_models
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
                 manufacture_methods=[]):
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


def get_sum_of_distribution_centers_redesign(shipping_distribution_cost,
                                    distribution_centers):
    sum_of_distribution_centers = 0
    for y in distribution_centers:
        sum_of_distribution_centers = sum_of_distribution_centers + \
                                      ((shipping_distribution_cost +
                                        y.transp_distribution_cost
                                        * 2 * y.distance_distribution)
                                       * y.distribution_selected)
    return sum_of_distribution_centers


def get_sum_of_disassembly_centers(shipping_disassembly_cost,
                                    disassembly_centers):
    sum_of_disassembly_centers = 0
    for y in disassembly_centers:
        sum_of_disassembly_centers = sum_of_distribution_centers + \
                                      ((shipping_disassembly_cost +
                                        y.transp_disassembly_cost
                                        * y.distance_disassembly)
                                       * y.disassembly_selected)
    return sum_of_disassembly_centers


def get_sum_of_manufacture_method(manufacture_methods, labor_cost):
    sum_of_manufacture_method = 0
    for y in manufacture_methods:
        sum_of_manufacture_method = sum_of_manufacture_method + \
                                    (y.hours_raw * labor_cost *
                                     y.manufacture_selected)
    return sum_of_manufacture_method


def get_sum_of_products_raw(models, generic_vals):
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
                                           i.manufacture_raw_cost)
    return sum_of_product


def get_sum_of_products_refurb(models, generic_vals):
    sum_of_product = 0
    for i in models:
        sum_of_storage_centers = \
            get_sum_of_storage_centers(i.shipping_storage_cost,
                                       i.storage_centers)
        sum_of_distribution_centers = \
            get_sum_of_distribution_centers(i.shipping_distribution_cost,
                                            i.distribution_centers)

        sum_of_disassembly_centers = \
            get_sum_of_disassembly_centers(i.shipping_disassembly_cost,
                                           i.disassembly_centers)



        sum_of_product = sum_of_product + (i.market_price_refurb -
                                           i.assembly_cost -
                                           sum_of_storage_centers -
                                           sum_of_distribution_centers -
                                           sum_of_disassembly_centers +
                                           generic_vals.defective_percentage/
                                           (1- generic_vals.defective_percentage)
                                           * sum_of_disassembly_centers -
                                           (i.hours_refurbished *
                                            generic_vals.labor_cost) -
                                           i.manufacture_refurbished_cost)
    return sum_of_product


def get_sum_of_products_redesign(models, generic_vals):
    sum_of_product = 0
    for i in models:
        sum_of_distribution_centers = \
            get_sum_of_distribution_centers_redesign(
                                            i.shipping_distribution_cost,
                                            i.distribution_centers)

        sum_of_product = sum_of_product + (i.market_price_redesign -
                                           sum_of_distribution_centers -
                                           (i.hours_redesigned *
                                            generic_vals.labor_cost))
    return sum_of_product

if __name__ == '__main__':

    raw_suppliers = []
    refurb_methods = []
    redesign_methods = []

    generic_vals = GenericValues()

    F1 = 0

    for raw_supplier in raw_suppliers:
        sum_of_products = get_sum_of_products_raw(raw_supplier.product_models,
                                              generic_vals)
        x_value = 0 # sum of t and i
        F1 = F1 + (sum_of_products -  raw_supplier.variable_raw_cost * x_value * raw_supplier.portion_raw)

    for raw_supplier in raw_suppliers:
        F1 = F1 - (raw_supplier.order_raw_cost *
                   raw_supplier.supplier_selected)


    for refurb_method in refurb_methods:
        sum_of_products = get_sum_of_products_refurb(
            refurb_methods.product_models, generic_vals)

        F1 = F1 - (sum_of_products - refurb_method.variable_refurbished_cost
                                    * ((1- generic_vals.defective_percentage)
                                    * refurb_method.portion_refurb *
                                      refurb_method.refurbish_method_capacity))

    for refurb_method in refurb_methods:
        F1 = F1 - (refurb_method.order_refurbish_cost *
                   refurb_method.refurbishment_selected)

    for redesign_method in redesign_methods:
        sum_of_products = get_sum_of_products_redesign(
            redesign_methods.product_models, generic_vals)

        F1 = F1 - (sum_of_products - redesign_method.variable_redesigned_cost
                   * (redesign_method.portion_redesign *
                      redesign_method.redesign_method_capacity) )

    for redesign_method in redesign_methods:
        F1 = F1 - (redesign_method.order_redesigned_cost *
                   redesign_method.redesign_selected)

