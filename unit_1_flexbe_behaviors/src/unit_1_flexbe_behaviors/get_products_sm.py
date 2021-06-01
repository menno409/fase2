#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.message_state import MessageState
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from unit_1_flexbe_behaviors.pick_part_from_bin_sm import pick_part_from_binSM
from unit_1_flexbe_behaviors.place_part_on_agv_sm import place_part_on_agvSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 19 2020
@author: Gerard Harkema
'''
class get_productsSM(Behavior):
	'''
	Getting all the products from a product list.

This example is a part of the order example.
	'''


	def __init__(self):
		super(get_productsSM, self).__init__()
		self.name = 'get_products'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(pick_part_from_binSM, 'pick_part_from_bin')
		self.add_behavior(place_part_on_agvSM, 'place_part_on_agv')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:719 y:341, x:826 y:25
		_state_machine = OperatableStateMachine(outcomes=['finished', 'fail'], input_keys=['Products', 'NumberOfProducts'])
		_state_machine.userdata.ProductIterator = 0
		_state_machine.userdata.OneValue = 1
		_state_machine.userdata.ProductType = ''
		_state_machine.userdata.ProductPose = ''
		_state_machine.userdata.Products = []
		_state_machine.userdata.NumberOfProducts = 0
		_state_machine.userdata.MaterialsLocationList = []
		_state_machine.userdata.MaterialLocation = ''
		_state_machine.userdata.MaterailLocationIndex = 0
		_state_machine.userdata.Robot_namespace = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:356 y:121
			OperatableStateMachine.add('GetProduct',
										GetPartFromProductsState(),
										transitions={'continue': 'ProductTypeMessage', 'invalid_index': 'fail'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'Products', 'index': 'ProductIterator', 'type': 'ProductType', 'pose': 'ProductPose'})

			# x:1226 y:120
			OperatableStateMachine.add('GerMaterailLocation',
										GetItemFromListState(),
										transitions={'done': 'MaterailLocationMessage', 'invalid_index': 'fail'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'MaterialsLocationList', 'index': 'MaterailLocationIndex', 'item': 'MaterialLocation'})

			# x:877 y:120
			OperatableStateMachine.add('GetMaterialsLocation',
										GetMaterialLocationsState(),
										transitions={'continue': 'MaterialsLocationListMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'ProductType', 'material_locations': 'MaterialsLocationList'})

			# x:817 y:258
			OperatableStateMachine.add('IncrementProductIterator',
										AddNumericState(),
										transitions={'done': 'CompareProductIterator'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'OneValue', 'result': 'ProductIterator'})

			# x:1406 y:124
			OperatableStateMachine.add('MaterailLocationMessage',
										MessageState(),
										transitions={'continue': 'pick_part_from_bin'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'MaterialLocation'})

			# x:1046 y:119
			OperatableStateMachine.add('MaterialsLocationListMessage',
										MessageState(),
										transitions={'continue': 'GerMaterailLocation'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'MaterialsLocationList'})

			# x:728 y:120
			OperatableStateMachine.add('ProductPoseMassage',
										MessageState(),
										transitions={'continue': 'GetMaterialsLocation'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ProductPose'})

			# x:569 y:121
			OperatableStateMachine.add('ProductTypeMessage',
										MessageState(),
										transitions={'continue': 'ProductPoseMassage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ProductType'})

			# x:1223 y:216
			OperatableStateMachine.add('pick_part_from_bin',
										self.use_behavior(pick_part_from_binSM, 'pick_part_from_bin'),
										transitions={'finished': 'place_part_on_agv', 'failed': 'fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'ProductType', 'robot_namespace': 'Robot_namespace', 'part_height_float': 'part_height_float'})

			# x:1011 y:247
			OperatableStateMachine.add('place_part_on_agv',
										self.use_behavior(place_part_on_agvSM, 'place_part_on_agv'),
										transitions={'finished': 'IncrementProductIterator', 'failed': 'fail'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ProductPose': 'ProductPose', 'robot_namespace': 'Robot_namespace', 'part_height_float': 'part_height_float'})

			# x:625 y:256
			OperatableStateMachine.add('CompareProductIterator',
										EqualState(),
										transitions={'true': 'finished', 'false': 'GetProduct'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'NumberOfProducts'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
