import math
import argparse
import yaml


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
                 inventory_cost, defective_percentage, labor_cost):
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
                 order_refurbish_cost,refurbishment_selected, portion_refurb,
                 product_models=[]):
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
                 order_redesign_cost, redesign_selected,
                 portion_redesign, product_models=[]):
        self.variable_redesigned_cost = variable_redesigned_cost
        self.redesign_method_capacity = redesign_method_capacity
        self.order_redesign_cost = order_redesign_cost
        self.product_models = product_models
        self.redesign_selected = redesign_selected
        self.portion_redesign = portion_redesign
    def __str__(self):
      return obj_to_string(self)

class Time:

    def __init__(self, interval_selected, time_period, up_bound, bound):
        self.time_period = time_period
        self.interval_selected = interval_selected
        self.up_bound = up_bound
        self.bound = bound
    def __str__(self):
      return obj_to_string(self)

class RawSupplier:

    def __init__(self, variable_raw_cost, order_raw_cost, 
                 portion_raw, supplier_selected, raw_capacity, product_models = [], times=[]):
        self.variable_raw_cost = variable_raw_cost
        self.order_raw_cost = order_raw_cost
        self.product_models = product_models
        self.portion_raw = portion_raw
        self.supplier_selected = supplier_selected
        self.raw_capacity = raw_capacity
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
        sum_of_disassembly_centers = sum_of_disassembly_centers + \
                                      ((shipping_disassembly_cost +
                                        y.transp_disassembly_cost
                                        * y.distance_disassembly)
                                       * y.disassembly_selected)
    return sum_of_disassembly_centers


def get_sum_of_disassembly_centers_f2(pollution_shipping_dissasembly,
                                    disassembly_centers):
    sum_of_disassembly_centers = 0
    for y in disassembly_centers:
        sum_of_disassembly_centers = sum_of_disassembly_centers + \
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
                                                     / (2 * i.number_raw))
    return sum_of_product_time

def get_sum_of_time_raw(times, models):
    sum_of_time_raw=0
    for time_i in times:
        sum_of_time_raw = sum_of_time_raw + (get_sum_of_products_time(models)
                                             * time_i.interval_selected)
    return sum_of_time_raw

def get_exp_given_severity_till_max(index, max_index):
    sum_of_exp_power = 0
    for i in range(index,max_index+1):
        sum_of_exp_power = sum_of_exp_power + (i/max_index)
    return math.exp(index-sum_of_exp_power)
    

def get_sum_of_manufactured_methods_severity(severities, raw_suppliers):
    max_index = len(severities)
    sum_of_severity_exp = 0
    for i in range(1,max_index+1):
        for manfacture_method in raw_suppliers[0].product_models[0].manufacture_methods:
            sum_of_severity_exp = sum_of_severity_exp + \
                                 get_exp_given_severity_till_max(i, max_index) \
                              * manfacture_method.manufacture_selected \
                              * manfacture_method.severity[i-1].severity_function_new
                        
    sum_of_raw_products = 0
    for raw_supplier in raw_suppliers:
        for product in raw_supplier.product_models:
            sum_of_raw_products = sum_of_raw_products + (
                                               (manfacture_method.hours_raw
                                               * raw_supplier.portion_raw
                                               * raw_supplier.raw_capacity))
 
    return sum_of_severity_exp * 20000 /sum_of_raw_products


def get_sum_of_refurb_methods_severity(severities, refurb_methods):
    max_index = len(severities)
    sum_of_severity_exp = 0
    for i in range(1,max_index+1):
        sum_of_severity_exp = sum_of_severity_exp + \
                            get_exp_given_severity_till_max(i, max_index) \
                            * severities[i-1].severity_function_refurbished
                        
    sum_of_refurb_products = 0
    for refurb_method in refurb_methods:
        for product in refurb_method.product_models:
            sum_of_refurb_products = sum_of_refurb_products + (
                                               (product.hours_refurbished
                                               * refurb_method.portion_refurb
                                               * refurb_method.refurbish_method_capacity))
 
    return sum_of_severity_exp * 20000 /sum_of_refurb_products


def get_sum_of_redesign_methods_severity(severities, redesign_methods):
    max_index = len(severities)
    sum_of_severity_exp = 0
    for i in range(1,max_index+1):
        sum_of_severity_exp = sum_of_severity_exp + \
                            get_exp_given_severity_till_max(i, max_index) \
                            * severities[i-1].severity_function_redesign
                        
    sum_of_redesign_products = 0
    for redesign_method in redesign_methods:
        for product in redesign_method.product_models:
            sum_of_redesign_products = sum_of_redesign_products + (
                                               (product.hours_redesigned
                                               * redesign_method.portion_redesign
                                               * redesign_method.redesign_method_capacity))
 
    return sum_of_severity_exp * 20000 /sum_of_redesign_products


def solve_f1(raw_suppliers, refurb_methods, redesign_methods , generic_vals):

    f1 = 0
    for raw_supplier in raw_suppliers:
        sum_of_products = get_sum_of_products_raw_f1(raw_supplier.product_models,
                                              generic_vals)
        sum_over_time = get_sum_of_time_raw(raw_supplier.times,
                                      raw_supplier.product_models)
        f1 = f1 + ((sum_of_products -
                   raw_supplier.variable_raw_cost)
                   * sum_over_time * raw_supplier.portion_raw)

    for raw_supplier in raw_suppliers:
        f1 = f1 - (raw_supplier.order_raw_cost *
                   raw_supplier.supplier_selected)


    for refurb_method in refurb_methods:
        sum_of_products = get_sum_of_products_refurb_f1(
            refurb_method.product_models, generic_vals)

        f1 = f1 - ((sum_of_products - refurb_method.variable_refurbished_cost)
                                    * ((1- generic_vals.defective_percentage)
                                    * refurb_method.portion_refurb *
                                      refurb_method.refurbish_method_capacity))

    for refurb_method in refurb_methods:
        f1 = f1 - (refurb_method.order_refurbish_cost *
                   refurb_method.refurbishment_selected)

    for redesign_method in redesign_methods:
        sum_of_products = get_sum_of_products_redesign_f1(
            redesign_method.product_models, generic_vals)

        f1 = f1 - ((sum_of_products - redesign_method.variable_redesigned_cost)
                   * (redesign_method.portion_redesign *
                      redesign_method.redesign_method_capacity) )

    for redesign_method in redesign_methods:
        f1 = f1 - (redesign_method.order_redesign_cost *
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

    f1 = f1 - (generic_vals.penalty_excess * (( generic_vals.initial_inventory
                                              + raw_inv
                + ((1-generic_vals.defective_percentage) * refurb_inv)
                + refurb_inv - generic_vals.demand
                - generic_vals.final_inventory)) - (generic_vals.inventory_cost \
         * generic_vals.final_inventory))

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
            raw_supplier.product_models, generic_vals)
        f2 = f2 + (sum_of_products
                   * ((1 - generic_vals.defective_percentage)
                      * refurb_method.portion_refurb *
                      refurb_method.refurbish_method_capacity))

    for redesign_method in redesign_methods:
        sum_of_products = get_sum_of_products_redesign_f2(
            redesign_method.product_models)

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


def _parse_command():
    parser = argparse.ArgumentParser(description='Optimization Model')
    parser.add_argument('--input-file', dest='input_file',
                        action='store', type=str,
                        required=True, help='Input file')
    return parser.parse_args()

if __name__ == '__main__':
    #parse_args = _parse_command()
    with open('test.yaml') as input_file:
      inputs = yaml.full_load(input_file)
    
    severities = []

    for severity in inputs['severity']:
      severities.append(Severity(severity, 0, inputs['severity'][severity]['severity_function_redesign'], inputs['severity'][severity]['severity_function_refurbished']))

    product_models = []
    for product in inputs['product']:
      storage_centers = []
      for storage_center in inputs['product'][product]['storage_centers']:
        storage_centers.append(StorageCenter(inputs['product'][product]['storage_centers'][storage_center]['transp_storage_cost'],inputs['product'][product]['storage_centers'][storage_center]['distance_storage'],inputs['product'][product]['storage_centers'][storage_center]['storage_selected']))
      distribution_centers = []
      for distribution_center in inputs['product'][product]['distribution_centers']:
        distribution_centers.append(DistributionCenter(inputs['product'][product]['distribution_centers'][distribution_center]['transp_distribution_cost'],inputs['product'][product]['distribution_centers'][distribution_center]['distance_distribution'],inputs['product'][product]['distribution_centers'][distribution_center]['distribution_selected']))
      disassembly_centers = []
      for disassembly_center in inputs['product'][product]['disassembly_centers']:
        disassembly_centers.append(DisassemblyCenter(inputs['product'][product]['disassembly_centers'][disassembly_center]['transp_disassembly_cost'],inputs['product'][product]['disassembly_centers'][disassembly_center]['distance_disassembly'],inputs['product'][product]['disassembly_centers'][disassembly_center]['disassembly_selected']))
      manufacture_methods = []
      for manufacture_method in inputs['product'][product]['manufacture_methods']:
        manufacture_severities = []
        for severity in inputs['product'][product]['manufacture_methods'][manufacture_method]['severity']:
          manufacture_severities.append(Severity(severity, inputs['product'][product]['manufacture_methods'][manufacture_method]['severity'][severity]['severity_function_new'], 0, 0))
        manufacture_methods.append(ManufactureMethod(inputs['product'][product]['manufacture_methods'][manufacture_method]['hours_raw'],inputs['product'][product]['manufacture_methods'][manufacture_method]['pollution_manufacturing'],inputs['product'][product]['manufacture_methods'][manufacture_method]['manufacture_selected'], manufacture_severities))

      product_models.append(ProductModel(inputs['product'][product]['market_price'],inputs['product'][product]['assembly_cost'],inputs['product'][product]['shipping_storage_cost'],inputs['product'][product]['shipping_distribution_cost'],inputs['product'][product]['manufacture_raw_cost'],inputs['product'][product]['market_price_refurb'],inputs['product'][product]['shipping_disassembly_cost'],inputs['product'][product]['hours_refurbished'],inputs['product'][product]['manufacture_refurbished_cost'],inputs['product'][product]['market_price_redesign'],inputs['product'][product]['hours_redesigned'],inputs['product'][product]['pollution_shipping_dissasembly'],inputs['product'][product]['pollution_shipping_storage'],inputs['product'][product]['pollution_refuribshed'],inputs['product'][product]['pollution_dissasembly'],inputs['product'][product]['pollution_shipping_distribution'],inputs['product'][product]['manufacture_raw_quantity'],inputs['product'][product]['raw_number'],storage_centers,distribution_centers,disassembly_centers,manufacture_methods))
    
    raw_suppliers = []
    for raw_supplier in inputs['raw_supplier']:
      times = []
      for time_i in inputs['raw_supplier'][raw_supplier]['times']:
        times.append(Time(inputs['raw_supplier'][raw_supplier]['times'][time_i]['interval_selected'],time_i, 0, 0))
      raw_suppliers.append(RawSupplier(inputs['raw_supplier'][raw_supplier]['variable_raw_cost'],inputs['raw_supplier'][raw_supplier]['order_raw_cost'],inputs['raw_supplier'][raw_supplier]['portion_raw'],inputs['raw_supplier'][raw_supplier]['supplier_selected'],inputs['raw_supplier'][raw_supplier]['raw_capacity'],product_models, times))

    refurb_methods = []
    for refurb_method in inputs['refurb_method']:
      refurb_methods.append(RefurbishmentMethod(inputs['refurb_method'][refurb_method]['variable_refurbished_cost'],inputs['refurb_method'][refurb_method]['refurbish_method_capacity'],inputs['refurb_method'][refurb_method]['order_refurbish_cost'],inputs['refurb_method'][refurb_method]['refurbishment_selected'],inputs['refurb_method'][refurb_method]['portion_refurb'],product_models))

    redesign_methods = []
    for redesign_method in inputs['redesign_method']:
      redesign_methods.append(RedesignMethod(inputs['redesign_method'][redesign_method]['variable_redesigned_cost'],inputs['redesign_method'][redesign_method]['redesign_method_capacity'],inputs['redesign_method'][redesign_method]['order_redesign_cost'],inputs['redesign_method'][redesign_method]['redesign_selected'],inputs['redesign_method'][redesign_method]['portion_redesign'],product_models))
   
    generic_vals = GenericValues(inputs['generic_values']['capacity_storage'],inputs['generic_values']['capacity_distribution'],inputs['generic_values']['capacity_disassembly'],inputs['generic_values']['returning_goal'],inputs['generic_values']['uncertain_demand'],inputs['generic_values']['penalty_excess'],inputs['generic_values']['initial_inventory'],inputs['generic_values']['demand'],inputs['generic_values']['final_inventory'],inputs['generic_values']['inventory_cost'],inputs['generic_values']['defective_percentage'],inputs['generic_values']['labor_cost'])

    f1 = solve_f1(raw_suppliers, refurb_methods, redesign_methods,
                  generic_vals)

    f2 = solve_f2(raw_suppliers, refurb_methods, redesign_methods,
                  generic_vals)
    
    f3 = solve_f3(severities, raw_suppliers, refurb_methods, redesign_methods,
                  generic_vals)
    
    print ('value of f1 : %s ' % f1)
    print ('value of f2 : %s ' % f2)
    print ('value of f3 : %s ' % f3)
