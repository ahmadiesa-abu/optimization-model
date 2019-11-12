import os
import time
import math


def obj_to_string(obj, extra='    '):
    return str(obj.__class__) + '\n' + '\n'.join(
        (extra + (str(item) + ' = ' +
                  (obj_to_string(obj.__dict__[item], extra + '    ') 
                   if hasattr(obj.__dict__[item], '__dict__') 
                   else str(obj.__dict__[item])))
         for item in sorted(obj.__dict__)))


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
    def __str__(self):
      return obj_to_string(self)


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
    def __str__(self):
      return obj_to_string(self)

class DisassemblyCenter:

    def __init__(self, transp_disassembly_cost, distance_disassembly,
                 disassembly_selected):
        self.transp_disassembly_cost = transp_disassembly_cost
        self.distance_disassembly = distance_disassembly
        self.disassembly_selected = disassembly_selected
    def __str__(self):
      return obj_to_string(self)

class Severity:

    def __init__(self, severity, severity_function_new, severity_function_redesign,
                 severity_function_refurbished):
        self.severity = severity
        self.severity_function_new = severity_function_new
        self.severity_function_redesign = severity_function_redesign
        self.severity_function_refurbished = severity_function_refurbished
    def __str__(self):
      return obj_to_string(self)
class ManufactureMethod:

    def __init__(self, hours_raw, pollution_manufacturing, manufacture_selected
                 , severity= []):
        self.hours_raw = hours_raw
        self.pollution_manufacturing = pollution_manufacturing
        self.manufacture_selected = manufacture_selected
        self.severity = severity


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
    def __str__(self):
      return obj_to_string(self)

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
    def __str__(self):
      return obj_to_string(self)

class Time:

    def __init__(self,product_models=[], interval_selected):
        self.product_models = product_models
        self.interval_selected = interval_selected
    def __str__(self):
      return obj_to_string(self)

class RawSupplier:

    def __init__(self, variable_raw_cost, order_raw_cost, product_models = [],
                 portion_raw, supplier_selected, times=[]):
        self.variable_raw_cost = variable_raw_cost
        self.order_raw_cost = order_raw_cost
        self.product_models = product_models
        self.portion_raw = portion_raw
        self.supplier_selected = supplier_selected
        self.times = times
    def __str__(self):
      return obj_to_string(self)

class ProductModel:

    def __init__(self, market_price, assembly_cost, shipping_storage_cost,
                 shipping_distribution_cost, manufacture_raw_cost,
                 market_price_refurb, shipping_disassembly_cost,
                 hours_refurbished, manufacture_refurbished_cost,
                 market_price_redesign, hours_redesigned,
                 pollution_shipping_dissasembly, pollution_shipping_storage,
                 pollution_refuribshed, pollution_dissasembly,
                 pollution_shipping_distribution,manufacture_raw_quantity,
                 number_raw, storage_centers=[],
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
        self.manufacture_raw_quantity =  manufacture_raw_quantity
        self.number_raw = number_raw
        self.storage_centers = storage_centers
        self.distribution_centers = distribution_centers
        self.disassembly_centers = disassembly_centers
        self.manufacture_methods = manufacture_methods
    def __str__(self):
      return obj_to_string(self)

def get_sum_of_storage_centers(shipping_storage_cost, storage_centers):
    sum_of_storage_centers = 0
    for y in storage_centers:
        sum_of_storage_centers = sum_of_storage_centers + \
                                 ((shipping_storage_cost +
                                   y.transp_storage_cost * y.distance_storage)
                                  * y.storage_selected)
    return sum_of_storage_centers

def get_sum_of_storage_centers_f2(pollution_shipping_storage, storage_centers):
    sum_of_storage_centers = 0
    for y in storage_centers:
        sum_of_storage_centers = sum_of_storage_centers + \
                                 (pollution_shipping_storage
                                   * y.distance_storage
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

def get_sum_of_distribution_centers_f2(pollution_shipping_distribution,
                                    distribution_centers):
    sum_of_distribution_centers = 0
    for y in distribution_centers:
        sum_of_distribution_centers = sum_of_distribution_centers + \
                                      (pollution_shipping_distribution
                                        * y.distance_distribution
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


def get_sum_of_distribution_centers_redesign_f2(pollution_shipping_distribution,
                                    distribution_centers):
    sum_of_distribution_centers = 0
    for y in distribution_centers:
        sum_of_distribution_centers = sum_of_distribution_centers + \
                                      (pollution_shipping_distribution
                                        * 2 * y.distance_distribution
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


def get_sum_of_disassembly_centers_f2(pollution_shipping_dissasembly,
                                    disassembly_centers):
    sum_of_disassembly_centers = 0
    for y in disassembly_centers:
        sum_of_disassembly_centers = sum_of_distribution_centers + \
                                      (pollution_shipping_dissasembly
                                        * y.distance_disassembly
                                       * y.disassembly_selected)
    return sum_of_disassembly_centers


def get_sum_of_manufacture_method(manufacture_methods, labor_cost):
    sum_of_manufacture_method = 0
    for y in manufacture_methods:
        sum_of_manufacture_method = sum_of_manufacture_method + \
                                    (y.hours_raw * labor_cost *
                                     y.manufacture_selected)
    return sum_of_manufacture_method


def get_sum_of_manufacture_method_f2(manufacture_methods):
    sum_of_manufacture_method = 0
    for y in manufacture_methods:
        sum_of_manufacture_method = sum_of_manufacture_method + \
                                    (y.pollution_manufacturing
                                    * y.manufacture_selected)
    return sum_of_manufacture_method


def get_sum_of_products_raw_f1(models, generic_vals):
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


def get_sum_of_products_raw_f2(models):
    sum_of_product = 0
    for i in models:
        sum_of_storage_centers = \
            get_sum_of_storage_centers_f2(i.pollution_shipping_storage,
                                       i.storage_centers)
        sum_of_distribution_centers = \
            get_sum_of_distribution_centers_f2(i.pollution_shipping_distribution,
                                            i.distribution_centers)

        sum_of_product = sum_of_product + (sum_of_storage_centers +
                                           sum_of_distribution_centers)
    return sum_of_product


def get_sum_of_products_refurb_f1(models, generic_vals):
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


def get_sum_of_products_refurb_f2(models, generic_vals):
    sum_of_product = 0
    for i in models:
        sum_of_storage_centers = \
            get_sum_of_storage_centers_f2(i.pollution_shipping_storage,
                                       i.storage_centers)
        sum_of_distribution_centers = \
            get_sum_of_distribution_centers_f2(i.pollution_shipping_distribution,
                                            i.distribution_centers)

        sum_of_disassembly_centers = \
            get_sum_of_disassembly_centers_f2(i.pollution_shipping_dissasembly,
                                           i.disassembly_centers)



        sum_of_product = sum_of_product + (sum_of_storage_centers +
                                           sum_of_distribution_centers +
                                           sum_of_disassembly_centers -
                                           generic_vals.defective_percentage/
                                           (1- generic_vals.defective_percentage)
                                           * sum_of_disassembly_centers )
    return sum_of_product

def get_sum_of_products_redesign_f1(models, generic_vals):
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


def get_sum_of_products_redesign_f2(models):
    sum_of_product = 0
    for i in models:
        sum_of_distribution_centers = \
            get_sum_of_distribution_centers_redesign_f2(
                                            i.pollution_shipping_distribution,
                                            i.distribution_centers)

        sum_of_product = sum_of_product + sum_of_distribution_centers
    return sum_of_product

def get_sum_of_products_raw_poll_f2(models):
    sum_of_product = 0
    for i in models:
        sum_of_manufacture =get_sum_of_manufacture_method_f2(
            i.manufacture_methods)

        sum_of_product = sum_of_product + sum_of_manufacture
    return sum_of_product

def get_sum_of_products_refub_poll_f2(models):
    sum_of_product = 0
    for i in models:
        sum_of_product = sum_of_product + i.pollution_refuribshed
    return sum_of_product


def get_sum_of_products_redesign_poll_f2(models):
    sum_of_product = 0
    for i in models:
        sum_of_product = sum_of_product + i.pollution_dissasembly
    return sum_of_product


def get_sum_of_products_time(models):
    sum_of_product_time = 0
    for i in models:
        sum_of_product_time = sum_of_product_time + (i.manufacture_raw_quantity
                                                     / 2 * i.number_raw)
    return sum_of_product_time

def get_sum_of_time_raw(times, models):
    sum_of_time_raw=0
    for time in times:
        sum_of_time_raw = sum_of_time_raw + (get_sum_of_products_time(models)
                                             * time.interval_selected)
    return sum_of_time_raw

def get_exp_given_severity_till_max(index, max_index)
    sum_of_exp_power = 0
    for i in range(index,max_index+1):
        sum_of_exp_power = sum_of_exp_power + (i/max_index)
    return math.exp(1-sum_of_exp_power)
    

def get_sum_of_manufactured_methods_severity(severities, raw_suppliers):
    sum_of_manufactured_methods_severity = 0
    max_index = len(severities)
    sum_of_severity_exp = 0
    for i in range(1,max_index+1):
        for manfacture_method in raw_suppliers.manfacture_methods:
            sum_of_severity_exp = sum_of_severity_exp+
                                get_exp_given_severity_till_max(i, max_index) *
                                manfacture_method.manufacture_selected *
                                manfacture_method.severity.severity_function_new
                        
    sum_of_raw_products = 0
    for raw_supplier in raw_suppliers:
        for product in raw_supplier.product_models:
            sum_of_raw_products = sum_of_raw_products + (20000 /
                                               manfacture_method.hours_raw
                                               * raw_supplier.portion_raw
                                               * raw_supplier.raw_capacity)
 
    return sum_of_severity_exp * sum_of_raw_products


def get_sum_of_refurb_methods_severity(severities, refurb_methods):
    sum_of_manufactured_methods_severity = 0
    max_index = len(severities)
    sum_of_severity_exp = 0
    for i in range(1,max_index+1):
        sum_of_severity_exp = sum_of_severity_exp+
                            get_exp_given_severity_till_max(i, max_index) *
                            severities[i-1].severity_function_refurbished
                        
    sum_of_refurb_products = 0
    for refurb_method in refurb_methods:
        for product in raw_supplier.product_models:
            sum_of_refurb_products = sum_of_refurb_products + (20000 /
                                               product.hours_refurbished
                                               * refurb_method.portion_refurb
                                               * refurb_method.refurbish_method_capacity)
 
    return sum_of_severity_exp * sum_of_refurb_products


def get_sum_of_redesign_methods_severity(severities, redesign_methods):
    sum_of_manufactured_methods_severity = 0
    max_index = len(severities)
    sum_of_severity_exp = 0
    for i in range(1,max_index+1):
        sum_of_severity_exp = sum_of_severity_exp+
                            get_exp_given_severity_till_max(i, max_index) *
                            severities[i-1].severity_function_redesign
                        
    sum_of_redesign_products = 0
    for redesign_method in redesign_methods:
        for product in raw_supplier.product_models:
            sum_of_redesign_products = sum_of_redesign_products + (20000 /
                                               product.hours_redesigned
                                               * redesign_method.portion_redesign
                                               * redesign_method.redesign_method_capacity)
 
    return sum_of_severity_exp * sum_of_redesign_products


def solve_f1(raw_suppliers, refurb_methods, redesign_methods , generic_vals):

    f1 = 0
    for raw_supplier in raw_suppliers:
        sum_of_products = get_sum_of_products_raw_f1(raw_supplier.product_models,
                                              generic_vals)
        sum_over_time = get_sum_of_time_raw(raw_supplier.times,
                                      raw_supplier.product_models)
        f1 = f1 + (sum_of_products -
                   raw_supplier.variable_raw_cost
                   * sum_over_time * raw_supplier.portion_raw)

    for raw_supplier in raw_suppliers:
        f1 = f1 - (raw_supplier.order_raw_cost *
                   raw_supplier.supplier_selected)


    for refurb_method in refurb_methods:
        sum_of_products = get_sum_of_products_refurb_f1(
            refurb_methods.product_models, generic_vals)

        f1 = f1 - (sum_of_products - refurb_method.variable_refurbished_cost
                                    * ((1- generic_vals.defective_percentage)
                                    * refurb_method.portion_refurb *
                                      refurb_method.refurbish_method_capacity))

    for refurb_method in refurb_methods:
        f1 = f1 - (refurb_method.order_refurbish_cost *
                   refurb_method.refurbishment_selected)

    for redesign_method in redesign_methods:
        sum_of_products = get_sum_of_products_redesign_f1(
            redesign_methods.product_models, generic_vals)

        f1 = f1 - (sum_of_products - redesign_method.variable_redesigned_cost
                   * (redesign_method.portion_redesign *
                      redesign_method.redesign_method_capacity) )

    for redesign_method in redesign_methods:
        f1 = f1 - (redesign_method.order_redesigned_cost *
                   redesign_method.redesign_selected)


    raw_inv = 0
    for raw_supplier in raw_suppliers:
        raw_inv = raw_inv + (raw_supplier.portion_raw
                             * raw_supplier.raw_capacity)

    refurb_inv = 0
    for refurb_method in refurb_methods:
        refurb_inv = refurb_inv + (refurb_method.portion_refurb *
                                   refurb_method.refurbish_method_capacity)

    redesign_inv = 0
    for redesign_method in redesign_methods:
        redesign_inv = redesign_inv + (redesign_method.portion_redesign *
                                       redesign_method.redesign_method_capacity)

    f1 = f1 - generic_vals.penalty_excess * (( generic_vals.initial_inventory
                                              + raw_inv
                + ((1-generic_vals.defective_percentage) * refurb_inv)
                + refurb_inv - generic_vals.demand
                - generic_vals.final_inventory)) - generic_vals.inventory_cost \
         * generic_vals.final_inventory

    return f1


def solve_f2(raw_suppliers, refurb_methods, redesign_methods , generic_vals):

    f2 = 0
    for raw_supplier in raw_suppliers:
        sum_of_products = get_sum_of_products_raw_f2(
            raw_supplier.product_models)

        f2 = f2 + (sum_of_products *
                   raw_supplier.portion_raw * raw_supplier.raw_capacity)

    for refurb_method in refurb_methods:
        sum_of_products = get_sum_of_products_refurb_f2(
            raw_supplier.product_models)
        f2 = f2 + (sum_of_products
                   * ((1 - generic_vals.defective_percentage)
                      * refurb_method.portion_refurb *
                      refurb_method.refurbish_method_capacity))

    for redesign_method in redesign_methods:
        sum_of_products = get_sum_of_products_redesign_f2(
            redesign_methods.product_models)

        f2 = f2 + (sum_of_products
                   * (redesign_method.portion_redesign *
                      redesign_method.redesign_method_capacity))

    for raw_supplier in raw_suppliers:
        sum_of_products = get_sum_of_products_raw_poll_f2(
            raw_supplier.product_models)

        f2 = f2 + (sum_of_products *
                   raw_supplier.portion_raw * raw_supplier.raw_capacity)

    for refurb_method in refurb_methods:
        sum_of_products = get_sum_of_products_refub_poll_f2(
            refurb_method.product_models)

        f2 = f2 + (sum_of_products *
                   refurb_method.portion_refurb *
                   refurb_method.refurbish_method_capacity)

    for redesign_method in redesign_methods:
        sum_of_products = get_sum_of_products_redesign_poll_f2(
            refurb_method.product_models)

        f2 = f2 + (sum_of_products *
                   redesign_method.portion_redesign *
                   redesign_method.redesign_method_capacity)

    return f2

def solve_f3(severities, raw_suppliers, refurb_methods,
             redesign_methods , generic_vals):

    f3 = 0
    f3 = f3 + get_sum_of_manufactured_methods_severity(severities, raw_suppliers) \
            + get_sum_of_refurb_methods_severity(severities, refurb_methods) \
            + get_sum_of_redesign_methods_severity(severities, redesign_methods)
    
    return f3


if __name__ == '__main__':
    severities = []
    product_models = []
    raw_suppliers = []
    refurb_methods = []
    redesign_methods = []

    generic_vals = GenericValues()

    f1 = solve_f1(raw_suppliers, refurb_methods, redesign_methods,
                  generic_vals)

    f2 = solve_f2(raw_suppliers, refurb_methods, redesign_methods,
                  generic_vals)
    
    f3 = solve_f3(raw_suppliers, refurb_methods, redesign_methods,
                  generic_vals)

