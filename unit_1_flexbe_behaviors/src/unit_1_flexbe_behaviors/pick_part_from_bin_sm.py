#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from ariac_support_flexbe_states.text_to_float_state import TextToFloatState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 25 2021
@author: docent
'''
class pick_part_from_binSM(Behavior):
	'''
	pick's a specific part form a it's bin
	'''


	def __init__(self):
		super(pick_part_from_binSM, self).__init__()
		self.name = 'pick_part_from_bin'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:139 y:319, x:449 y:445
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part', 'robot_namespace'])
		_state_machine.userdata.robot_namespace = ''
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.zero = 0
		_state_machine.userdata.config_name_home = 'home'
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = 'ariac/arm1'
		_state_machine.userdata.robotname = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.camera_reference_frame = 'arm1_linear_arm_actuator'
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.part_height = ''
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.gripper_service = '/ariac/arm1/gripper/control'
		_state_machine.userdata.locations = []
		_state_machine.userdata.bin = ''
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.part = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('Start',
										StartAssignment(),
										transitions={'continue': 'Move home'},
										autonomy={'continue': Autonomy.Off})

			# x:1149 y:500
			OperatableStateMachine.add('Compute pick',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'Activate gripper', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_height_float', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1104 y:174
			OperatableStateMachine.add('Detect part',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'fout vinden', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'camera_reference_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:68 y:553
			OperatableStateMachine.add('End',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:565 y:37
			OperatableStateMachine.add('Get bin from locations',
										GetItemFromListState(),
										transitions={'done': 'Look up camera topic', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'locations', 'index': 'zero', 'item': 'bin'})

			# x:372 y:35
			OperatableStateMachine.add('Get part location',
										GetMaterialLocationsState(),
										transitions={'continue': 'Get bin from locations'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'part', 'material_locations': 'locations'})

			# x:934 y:24
			OperatableStateMachine.add('Look up camera frame',
										LookupFromTableState(parameter_name="ariac_tables_unit1", table_name='bin_configuration', index_title='bin', column_title='camera_frame'),
										transitions={'found': 'Look up pregrasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:761 y:24
			OperatableStateMachine.add('Look up camera topic',
										LookupFromTableState(parameter_name="ariac_tables_unit1", table_name="bin_configuration", index_title='bin', column_title='camera_topic'),
										transitions={'found': 'Look up camera frame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:1114 y:8
			OperatableStateMachine.add('Look up pregrasp',
										LookupFromTableState(parameter_name="ariac_tables_unit1", table_name='bin_configuration', index_title='bin', column_title='robot_config'),
										transitions={'found': 'look up string', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_config'})

			# x:204 y:37
			OperatableStateMachine.add('Move home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Get part location', 'planning_failed': 'Wait retry', 'control_failed': 'Wait retry', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_home', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robotname', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:258 y:567
			OperatableStateMachine.add('Move home2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'End', 'planning_failed': 'wait retry2', 'control_failed': 'wait retry2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_home', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robotname', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1151 y:428
			OperatableStateMachine.add('Move pregrasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Compute pick', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robotname', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:480 y:569
			OperatableStateMachine.add('Move to pick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Move home2', 'planning_failed': 'wait retry 3', 'control_failed': 'wait retry 3'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:225 y:156
			OperatableStateMachine.add('Wait retry',
										WaitState(wait_time=1),
										transitions={'done': 'Move home'},
										autonomy={'done': Autonomy.Off})

			# x:1144 y:265
			OperatableStateMachine.add('fout vinden',
										MessageState(),
										transitions={'continue': 'omzetten'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part'})

			# x:1130 y:78
			OperatableStateMachine.add('look up string',
										LookupFromTableState(parameter_name="ariac_tables_unit1", table_name="part_height_configuration", index_title='part', column_title='part_height'),
										transitions={'found': 'Detect part', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'part', 'column_value': 'part_height'})

			# x:1133 y:364
			OperatableStateMachine.add('omzetten',
										TextToFloatState(),
										transitions={'done': 'Move pregrasp'},
										autonomy={'done': Autonomy.Off},
										remapping={'text_value': 'part_height', 'float_value': 'part_height_float'})

			# x:525 y:663
			OperatableStateMachine.add('wait retry 3',
										WaitState(wait_time=1),
										transitions={'done': 'Move to pick'},
										autonomy={'done': Autonomy.Off})

			# x:285 y:655
			OperatableStateMachine.add('wait retry2',
										WaitState(wait_time=1),
										transitions={'done': 'Move home2'},
										autonomy={'done': Autonomy.Off})

			# x:756 y:570
			OperatableStateMachine.add('Activate gripper',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'Move to pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
