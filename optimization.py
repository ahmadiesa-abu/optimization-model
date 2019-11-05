import os
import time

class ProductModel:

	def __init__(self, raw_supplier, product, raw_material,
			time_supplied, refurbishment_meth, 
			redesign_method, inventory, storage_center,
			distribution_center, disassembly_center, 
			manufacture_method, severity,market_price,
			assembly_cost, shipping_storage_cost,
			transp_storage_cost,distance_storage,
			shipping_distribution_cost, transp_distribution_cost,
			distance_distribution, hours_raw, labor_cost,
			manufacture_raw_cost, variable_raw_cost,
			raw_capacity, manufacture_raw_cost, number_raw,
			order_raw_cost, market_price_refurb,
			variable_refurbished_cost, shipping_disassembly_cost,
			transp_disassembly_cost, distance_disassembly,
			defective_percentage, hours_refurbished,
			manufacture_refurbished_cost, refurbish_method_capacity,
			order_refurbish_cost, market_price_redesign,
			hours_redesigned,redesign_method_capacity, order_redesign_cost,
			penalty_excess, initial_inventory, demand,
			final_inventory, inventory_cost, pollution_shipping_dissasembly,
			pollution_manufacturing, pollution_shipping_storage,
			pollution_refuribshed, pollution_dissasembly, pollution_shipping_distribution,
			severity_function_new, severity_function_refurbished, severity_function_redesign,
			capacity_storage, capacity_distribution, capacity_disassembly, 
			returning_goal, uncertain_demand, up_bound, bound):
		self.raw_supplier = raw_supplier
		self.time_supplied = time_supplied
		self.redesign_method = redesign_method
		self.distribution_center = distribution_center
		self.manufacture_method = manufacture_method
		self.assembly_cost = assembly_cost
		self.transp_storage_cost = transp_storage_cost
		self.shipping_distribution_cost = shipping_distribution_cost
		self.distance_distribution = distance_distribution
		self.manufacture_raw_cost = manufacture_raw_cost
		self.raw_capacity = raw_capacity
		self.order_raw_cost = order_raw_cost
		self.variable_refurbished_cost = variable_refurbished_cost
		self.transp_disassembly_cost = transp_disassembly_cost
		self.defective_percentage = defective_percentage
		self.manufacture_refurbished_cost = manufacture_refurbished_cost
		self.order_refurbish_cost = order_refurbish_cost
		self.hours_redesigned = hours_redesigned
		self.redesign_method_capacity = redesign_method_capacity
		self.penalty_excess = penalty_excess
		self.final_inventory = final_inventory
		self.pollution_manufacturing = pollution_manufacturing
		self.pollution_refuribshed = pollution_refuribshed
		self.severity_function_new = severity_function_new
		self.capacity_storage = capacity_storage
		self.returning_goal = returning_goal
		self.product = product
		self.refurbishment_meth = refurbishment_meth
		self.inventory = inventory
		self.disassembly_center = disassembly_center
		self.severity = severity
		self.shipping_storage_cost = shipping_storage_cost
		self.distance_storage = distance_storage
		self.transp_distribution_cost = transp_distribution_cost
		self.hours_raw = hours_raw
		self.variable_raw_cost = variable_raw_cost
		self.market_price_refurb = market_price_refurb
		self.shipping_disassembly_cost = shipping_disassembly_cost
		self.distance_disassembly = distance_disassembly
		self.hours_refurbished = hours_refurbished
		self.refurbish_method_capacity = refurbish_method_capacity
		self.market_price_redesign = market_price_redesign
		self.order_redesign_cost = order_redesign_cost
		self.initial_inventory = initial_inventory
		self.inventory_cost = inventory_cost
		self.pollution_shipping_storage = pollution_shipping_storage
		self.pollution_dissasembly = pollution_dissasembly
		self.severity_function_refurbished = severity_function_refurbished
		self.capacity_distribution = capacity_distribution
		self.uncertain_demand = uncertain_demand
		self.raw_material = raw_material
		self.storage_center = storage_center
		self.market_price = market_price
		self.labor_cost = labor_cost
		self.number_raw = number_raw
		self.demand = demand
		self.pollution_shipping_dissasembly = pollution_shipping_dissasembly
		self.pollution_shipping_distribution = pollution_shipping_distribution
		self.severity_function_redesign = severity_function_redesign
		self.capacity_disassembly = capacity_disassembly
		self.up_bound = up_bound
		self.bound = bound


def array_sum(array_values):
	result = 0
	for i in array_values:
		result = result + i
	return result

if __name__=='__main__':
	ProductModel m1 = ProductModel()

