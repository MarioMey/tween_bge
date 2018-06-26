'''
tween para BGE, v0.93
Mario Mey - http://www.mariomey.com.ar

Based in Tweener, for ActionScript 2 and 3.
https://code.google.com/p/tweener/

Using Robert Penner's Easing Functions
http://www.robertpenner.com/easing/
'''

import bge, mathutils, time

gd = bge.logic.globalDict
current_scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()

getScene = {}
for a in bge.logic.getSceneList():
	getScene[a.name] = a

# Un solo objeto es el que maneja todos los tweens (el que ejecuta
# el codigo), independiente de que objetos esten siendo afectados.
own = cont.owner

#~ print_all_data = False
print_obj_move = False
print_obj_rotate = False
print_obj_scale = False
print_obj_property = False
print_obj_color = False
print_obj_diff_color = False
print_bone_move = False
print_constraint_enforce = False
print_obj_no_obj_change = False

print_all_data = True
#~ print_obj_move = True
#~ print_obj_rotate = True
#~ print_obj_scale = True
#~ print_obj_property = True
#~ print_obj_color = True
#~ print_obj_diff_color = True
#~ print_bone_move = True
#~ print_constraint_enforce = True
#~ print_obj_no_obj_change = True

# TWEEN - Principal, hace funcionar el Loop
def tween(**kwargs):
	
	# Escena inicial
	scene = current_scene.name
	
	# Objeto inicial (puede ser otro)
	obj = own.name
	
	# claves y valores por defecto
	function = ''
	element = own.name
	
	prop_value_begin = None
	prop_value = None
	
	enforce_begin = None
	enforce = None
	
	color_begin = None
	color = None

	loc_obj_begin = None
	loc_begin = None
	loc_obj_target = None
	loc_target = None

	rot_obj_begin = None
	rot_begin = None
	rot_obj_target = None
	rot_target = None

	scl_obj_begin = None
	scl_begin = None
	scl_obj_target = None
	scl_target = None

	delay = 0
	duration = 1.0
	ease_type = 'outQuad'
	
	send_message_on_end = None
	
	obj_prop_on_start = None
	obj_prop_on_start_value = None
	obj_prop_on_end = None
	obj_prop_on_end_value = None
	
	gd_key_on_start = None
	gd_key_on_start_value = None
	gd_key_on_end = None
	gd_key_on_end_value = None
	
	seg_orden_on_end = None
	
	# ERRORES ERRORES ERRORES
	# ... aca para poder usar scene como objeto
	#~ print(getScene['principal'].objects)
	if 'scene' in kwargs and kwargs['scene'] not in getScene:
		print(kwargs)
		print('Tween Error. No existe la escena:', kwargs['scene'])
		return
	# ERRORES ERRORES ERRORES
		

	if 'scene' in kwargs:               scene                  = kwargs['scene']
	
	if 'element' in kwargs:             element                = kwargs['element']

	if 'prop_value_begin' in kwargs:    prop_value_begin       = kwargs['prop_value_begin']
	if 'prop_value' in kwargs:          prop_value             = kwargs['prop_value']
	
	if 'enforce_begin' in kwargs:       enforce_begin          = kwargs['enforce_begin']
	if 'enforce' in kwargs:             enforce                = kwargs['enforce']

	if 'color_begin' in kwargs:         color_begin            = kwargs['color_begin']
	if 'color' in kwargs:               color                  = kwargs['color']

	if 'loc_obj_begin' in kwargs:       loc_obj_begin          = kwargs['loc_obj_begin']
	if 'loc_begin' in kwargs:           loc_begin              = kwargs['loc_begin']
	if 'loc_obj_target' in kwargs:      loc_obj_target         = kwargs['loc_obj_target']
	if 'loc_target' in kwargs:          loc_target             = kwargs['loc_target']

	if 'rot_obj_begin' in kwargs:       rot_obj_begin          = kwargs['rot_obj_begin']
	if 'rot_begin' in kwargs:           rot_begin              = kwargs['rot_begin']
	if 'rot_obj_target' in kwargs:      rot_obj_target         = kwargs['rot_obj_target']
	if 'rot_target' in kwargs:          rot_target             = kwargs['rot_target']

	if 'scl_obj_begin' in kwargs:       scl_obj_begin          = kwargs['scl_obj_begin']
	if 'scl_begin' in kwargs:           scl_begin              = kwargs['scl_begin']
	if 'scl_obj_target' in kwargs:      scl_obj_target         = kwargs['scl_obj_target']
	if 'scl_target' in kwargs:          scl_target             = kwargs['scl_target']

	if 'delay' in kwargs:               delay                  = kwargs['delay']
	if 'duration' in kwargs:            duration               = kwargs['duration']
	if 'ease_type' in kwargs:           ease_type              = kwargs['ease_type']
	
	if 'send_message_on_end' in kwargs:       send_message_on_end          = kwargs['send_message_on_end']
	
	if 'obj_prop_on_start' in kwargs:       obj_prop_on_start          = kwargs['obj_prop_on_start']
	if 'obj_prop_on_start_value' in kwargs: obj_prop_on_start_value    = kwargs['obj_prop_on_start_value']
	if 'obj_prop_on_end' in kwargs:         obj_prop_on_end            = kwargs['obj_prop_on_end']
	if 'obj_prop_on_end_value' in kwargs:   obj_prop_on_end_value      = kwargs['obj_prop_on_end_value']

	if 'gd_key_on_start' in kwargs:       gd_key_on_start          = kwargs['gd_key_on_start']
	if 'gd_key_on_start_value' in kwargs: gd_key_on_start_value    = kwargs['gd_key_on_start_value']
	if 'gd_key_on_end' in kwargs:         gd_key_on_end            = kwargs['gd_key_on_end']
	if 'gd_key_on_end_value' in kwargs:   gd_key_on_end_value      = kwargs['gd_key_on_end_value']

	if 'seg_orden_on_end' in kwargs:   seg_orden_on_end      = kwargs['seg_orden_on_end']
	
	# Imprime siempre toda la data ingresada
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_all_data:
		print(kwargs)
	# ERRORES ERRORES ERRORES
	# ERRORES ERRORES ERRORES
	# ERRORES ERRORES ERRORES
	
	# si no se ingreso ningun dato.
	cond1 = loc_obj_target == loc_target == None
	cond2 = rot_obj_target == rot_target == None
	cond3 = scl_obj_target == scl_target == None
	cond4 = prop_value == color == enforce == None
	cond5 = seg_orden_on_end == None
	cond6 = send_message_on_end == None
	if cond1 and cond2 and cond3 and cond4 and cond5 and cond6:
		print('Tween Error. Falta, al menos, uno de los siguientes datos:')
		print('       loc_obj_target, loc_target,')
		print('       rot_obj_target, rot_target,')
		print('       scl_obj_target, scl_target,')
		print('       prop_value, color, enforce,')
		print('       seg_orden_on_end, send_message_on_end')
		return
	
	# para evitar multiples acciones
	cond1 = loc_obj_begin != None or loc_begin != None or loc_obj_target != None or loc_target != None
	cond2 = rot_obj_begin != None or rot_begin != None or rot_obj_target != None or rot_target != None
	cond3 = scl_obj_begin != None or scl_begin != None or scl_obj_target != None or scl_target != None
	cond4 = color_begin != None or color != None
	cond5 = enforce_begin != None or enforce != None
	cond6 = prop_value != None
	if int(cond1) + int(cond2) + int(cond3) + int(cond4) + int(cond5) + int(cond6) > 1 :
		print('Tween Error. Por favor, de a una accion a la vez.')
		return
	
	cond1 = loc_obj_begin != None and loc_obj_begin not in getScene[scene].objects
	cond2 = loc_obj_target != None and loc_obj_target not in getScene[scene].objects
	cond3 = rot_obj_begin != None and rot_obj_begin not in getScene[scene].objects
	cond4 = rot_obj_target != None and rot_obj_target not in getScene[scene].objects
	cond5 = scl_obj_begin != None and scl_obj_begin not in getScene[scene].objects
	cond6 = scl_obj_target != None and scl_obj_target not in getScene[scene].objects
	if cond1 or cond2 or cond3 or cond4 or cond5 or cond6:
		print('Tween Error. No existe el objeto de referencia')
		return
		
	
	# para evitar mover un bone a un worldLocation
	if len(element.split(':')) == 2 and (loc_obj_begin != None or loc_obj_target != None):
		print('Tween Error. Por el momento, no se puede mover un bone a/de un Word Location')
		return
	
	# si no se asigna un valor a obj_prop_on_start o obj_prop_on_end
	if obj_prop_on_start != None and obj_prop_on_start_value == None:
		print('Tween Error. No se asigno un valor a obj_prop_on_start')
		return

	if obj_prop_on_end != None and obj_prop_on_end_value == None:
		print('Tween Error. No se asigno un valor a obj_prop_on_end')
		return

	if prop_value != None and element.split(':') == 1 and element not in own:
		print('Tween Error. No existe la propiedad del objeto:', own.name)
		return

	if prop_value != None and element.split(':') == 2 and element.split(':')[1] not in getScene[scene].objects[element.split(':')[0]]:
		print('Tween Error. No existe la propiedad del objeto: ', element.split(':')[0])
		return

	# si send_message_on_end no es una lista
	if send_message_on_end != None and type(send_message_on_end) is not list:
		print('Tween Error. send_message_on_end debe ser una lista de dos elementos: [subject, body]')
		return

	# si send_message_on_end es una lista de != 2 elementos
	if send_message_on_end != None and type(send_message_on_end) is list and len(send_message_on_end) != 2:
		print('Tween Error. send_message_on_end debe ser una lista de dos elementos: [subject, body]')
		return

	#~ if prop_value != None and (type(prop_value) == int or type(prop_value) == float:
		#~ print('Error. Valores en int o float para prop_value')
		#~ return

	
	# FIN - ERRORES
	# FIN - ERRORES
	# FIN - ERRORES
	element = element.split(':')
	obj = element[0]
	
	# Propiedad (clave) de objeto
	if prop_value != None:
		# si es 'prop' sin objeto, arregla 'element', pasa a ser ['objeto', 'prop']
		if len(element) == 1:
			element = [own.name, element[0]]
			# ... y obj pasa a recibir el nombre de own.
			obj = element[0]

		function = 'property'
		if prop_value_begin == None:
			prop_value_begin = getScene[scene].objects[obj][element[1]]
	
	else:
		# objeto
		if len(element) == 1:
			# si es para mover un obj, setea loc_begin[x,y,z]
			# dejando '' si no tiene nada.
			if loc_obj_target != None or loc_target != None:
				function = 'obj_move'

				if loc_begin == None and loc_obj_begin == None:
					loc_begin = list(getScene[scene].objects[obj].worldPosition)
			
				elif loc_obj_begin != None:
					loc_begin = list(getScene[scene].objects[loc_obj_begin].worldPosition)

				if loc_begin == loc_target:
					if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
						print('--TWEEN - obj: ' + obj, end='')
						print(' - loc_begin = loc_target -> Nada para hacer')
					return
			
			# si es para rotar un obj, setea rot_begin[x,y,z]
			# dejando '' si no tiene nada.
			if rot_obj_target != None or rot_target != None:
				function = 'obj_rotate'

				if rot_begin == None and rot_obj_begin == None:
					rot_begin = list(getScene[scene].objects[obj].worldOrientation.to_euler())
			
				elif rot_obj_begin != None:
					rot_begin = list(getScene[scene].objects[rot_obj_begin].worldOrientation.to_euler())

				if rot_begin == rot_target:
					if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
						print('--TWEEN - obj: ' + obj, end='')
						print(' - rot_begin = rot_target -> Nada para hacer')
					return
			
			# si es para escalar un obj, setea scl_begin[x,y,z]
			# dejando '' si no tiene nada.
			if scl_obj_target != None or scl_target != None:
				function = 'obj_scale'

				if scl_begin == None and scl_obj_begin == None:
					scl_begin = list(getScene[scene].objects[obj].worldScale)
			
				elif scl_obj_begin != None:
					scl_begin = list(getScene[scene].objects[scl_obj_begin].worldScale)
				
				if scl_begin == scl_target:
					if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
						print('--TWEEN - obj: ' + obj, end='')
						print(' - scl_begin = scl_target -> Nada para hacer')
					return
			
			# si es para cambiar color de un obj, setea color_begin[r,g,b,a]
			if color != None :
				function = 'obj_color'

				if color_begin == None:
					color_begin = list(getScene[scene].objects[obj].color)
					
				if color_begin == color:
					if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
						print('--TWEEN - obj: ' + obj, end='')
						print(' - color_begin = color -> Nada para hacer')
					return
			
			# Para funciones en objeto sin cambios en Loc, Rot, Scl o Color.
			# Ej: send_message_on_end, seg_orden_on_end, etc.
			cond1 = loc_obj_target == None and loc_target == None
			cond2 = rot_obj_target == None and rot_target == None
			cond3 = scl_obj_target == None and scl_target == None
			cond4 = color == None
			
			cond5 = send_message_on_end != None
			cond6 = seg_orden_on_end != None
			cond7 = obj_prop_on_end != None
			cond8 = gd_key_on_end != None
			
			if cond1 and cond2 and cond3 and cond4 and (cond5 or cond6 or cond7 or cond8):
				function = 'noObjLocRotSclColChange'
			
		# bone en Local
		# si es para mover un bone, setea begin[x,y,z] del bone
		elif len(element) == 2:
			function = 'bone_move'
			if loc_begin == None:
				arm = getScene[scene].objects[obj]
				bone = element[1]
				loc_begin = list(arm.channels[bone].location)
				
			if loc_begin == loc_target:
				if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
					print('--TWEEN - obj: ' + obj, end='')
					print(' - loc_begin = loc_target -> Nada para hacer')
				return

		# constraint
		elif len(element) == 3:
			function = 'constraint_enforce'
			if enforce_begin == None:
				arm = getScene[scene].objects[obj]
				bone_constraint = element[1] + ':' + element[2]
				enforce_begin = arm.constraints[bone_constraint].enforce
				
			if float(enforce_begin) == float(enforce):
				if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
					print('--TWEEN - obj: ' + obj, end='')
					print(' - enforce_begin = enforce -> Nada para hacer')
				return

	number = -1
	
	# Escanea si existe own['tween1 -> 16']
	# Si esta en uso, pero es del mismo objeto y
	# la misma funcion, la borra y la usa
	for i in range(16):
		
		num = str(i)
		if 'tween' + num in own:
			cond1 = own['tween' + num]['function'] == function
			cond2 = own['tween' + num]['element'] == element
			if cond1 and cond2:
				
				# function a ejecutar cuando termina, si se corta antes
				if own['tween' + num]['obj_prop_on_end'] != None:
					prop = own['tween' + num]['obj_prop_on_end']
					value = own['tween' + num]['obj_prop_on_end_value']
					getScene[scene].objects[obj][prop] = value

				del(own['tween' + num])
				number = i
				break
	
	# Si no encontro para reemplazar, de nuevo,
	# Escanea si existe own['tween1 -> 16']
	if number == -1:
		for i in range(16):
			
			num = str(i)
			if 'tween' + num in own:
				# Sigue contando
				continue
			
			# Encontro uno libre
			number = i
			break
	
	number = str(number)

	own['tween' + number]                        = {}
	own['tween' + number]['scene']               = getScene[scene].name
	own['tween' + number]['obj']                 = obj

	own['tween' + number]['number']              = number
	own['tween' + number]['function']            = function
	own['tween' + number]['element']             = element
	
	own['tween' + number]['prop_value_begin']    = prop_value_begin
	own['tween' + number]['prop_value']          = prop_value
	
	own['tween' + number]['enforce_begin']       = enforce_begin
	own['tween' + number]['enforce']             = enforce

	own['tween' + number]['color_begin']         = color_begin
	own['tween' + number]['color']               = color
	
	own['tween' + number]['loc_begin']           = loc_begin
	own['tween' + number]['loc_obj_target']      = loc_obj_target
	own['tween' + number]['loc_target']          = loc_target

	own['tween' + number]['rot_begin']           = rot_begin
	own['tween' + number]['rot_obj_target']      = rot_obj_target
	own['tween' + number]['rot_target']          = rot_target

	own['tween' + number]['scl_begin']           = scl_begin
	own['tween' + number]['scl_obj_target']      = scl_obj_target
	own['tween' + number]['scl_target']          = scl_target

	own['tween' + number]['enforce']             = enforce
	own['tween' + number]['enforce_begin']       = enforce_begin

	own['tween' + number]['duration']            = duration
	own['tween' + number]['delay']               = delay
	own['tween' + number]['ease_type']           = ease_type
	
	own['tween' + number]['send_message_on_end']       = send_message_on_end
	
	own['tween' + number]['obj_prop_on_start']       = obj_prop_on_start
	own['tween' + number]['obj_prop_on_start_value'] = obj_prop_on_start_value
	own['tween' + number]['obj_prop_on_end']         = obj_prop_on_end
	own['tween' + number]['obj_prop_on_end_value']   = obj_prop_on_end_value
	
	own['tween' + number]['gd_key_on_start']       = gd_key_on_start
	own['tween' + number]['gd_key_on_start_value'] = gd_key_on_start_value
	own['tween' + number]['gd_key_on_end']         = gd_key_on_end
	own['tween' + number]['gd_key_on_end_value']   = gd_key_on_end_value
	
	own['tween' + number]['seg_orden_on_end']    = seg_orden_on_end
	
	own['tween' + number]['timer'] = time.time()

	# PRINT TWEEN FUNCIONES
	if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
		
		texto = '\n'
		texto += '--TWEEN' + number + ' - scene: ' + getScene[scene].name + ' - obj: ' + obj + '\n'
		texto += '--' + function + str(element) + '\n'
		texto += '--delay: '+ str(delay) + ' '
		texto += '--duration: ' + str(duration) + ' '
		texto += '--ease_type: ' + ease_type + '\n'
		
		if enforce != None:
			texto += '--enforce: ' + str(enforce)

			if enforce_begin != None:
				texto += ' --enforce_begin: ' + str(enforce_begin)
			
			texto += '\n'

		if color != None:
			texto += '--color: ' + str(color)

			if color_begin != None:
				texto += ' --color_begin: ' + str(color_begin)
			
			texto += '\n'

		if prop_value != None:
			texto += '--prop_value: ' + str(prop_value)

			if prop_value_begin != None:
				texto += ' --prop_value_begin: ' + str(prop_value_begin)
			
			texto += '\n'

		if loc_begin != None:
			texto += '--loc_begin: ' + str(loc_begin) + '\n'
		
		if loc_obj_begin != None:
			texto += '--loc_obj_begin: ' + loc_obj_begin + '\n'
		
		if loc_target != None:
			texto += '--loc_target: ' + str(loc_target) + '\n'

		if loc_obj_target != None:
			texto += '--loc_obj_target: ' + loc_obj_target + '\n'

		if rot_begin != None:
			texto += '--rot_begin: ' + str(rot_begin) + '\n'

		if rot_obj_begin != None:
			texto += '--rot_obj_begin: ' + rot_obj_begin + '\n'

		if rot_target != None:
			texto += '--rot_target: ' + str(rot_target) + '\n'

		if rot_obj_target != None:
			texto += '--rot_obj_target: ' + rot_obj_target + '\n'

		if scl_begin != None:
			texto += '--scl_begin: ' + str(scl_begin) + '\n'

		if  scl_obj_begin != None:
			texto += '--scl_obj_begin: ' + scl_obj_begin + '\n'

		if scl_target != None:
			texto += '--scl_target: ' + str(scl_target) + '\n'

		if scl_obj_target != None:
			texto += '--scl_obj_target: ' + scl_obj_target + '\n'

		if send_message_on_end != None:
			texto += '--send_message_on_end: ' + str(send_message_on_end) + '\n'

		if obj_prop_on_start != None:
			texto += '--obj_prop_on_start: ' + str(obj_prop_on_start) + ':' + str(obj_prop_on_start_value) + '\n'

		if obj_prop_on_end != None:
			texto += '--obj_prop_on_end: ' + str(obj_prop_on_end) + ':' + str(obj_prop_on_end_value) + '\n'

		if gd_key_on_start != None:
			texto += '--gd_key_on_start: ' + str(gd_key_on_start) + ':' + str(gd_key_on_start_value) + '\n'

		if gd_key_on_end != None:
			texto += '--gd_key_on_end: ' + str(gd_key_on_end) + ':' + str(gd_key_on_end_value) + '\n'

		if seg_orden_on_end != None:
			texto += '--seg_orden_on_end: ' + seg_orden_on_end
		
		print(texto)




# TWEEN - Loop
def tween_loop():
	
	for i in range(16):
		number = str(i)

		if 'tween' + number in own:
			
			scene               = own['tween' + number]['scene']
			obj                 = own['tween' + number]['obj']
			function            = own['tween' + number]['function']
			element             = own['tween' + number]['element']
			
			prop_value_begin    = own['tween' + number]['prop_value_begin']
			prop_value          = own['tween' + number]['prop_value']
			
			enforce_begin       = own['tween' + number]['enforce_begin']
			enforce             = own['tween' + number]['enforce']
			
			color_begin         = own['tween' + number]['color_begin']
			color               = own['tween' + number]['color']
			
			loc_begin           = own['tween' + number]['loc_begin']
			loc_obj_target      = own['tween' + number]['loc_obj_target']
			loc_target          = own['tween' + number]['loc_target']

			rot_begin           = own['tween' + number]['rot_begin']
			rot_obj_target      = own['tween' + number]['rot_obj_target']
			rot_target          = own['tween' + number]['rot_target']

			scl_begin           = own['tween' + number]['scl_begin']
			scl_obj_target      = own['tween' + number]['scl_obj_target']
			scl_target          = own['tween' + number]['scl_target']

			delay               = own['tween' + number]['delay']
			duration            = own['tween' + number]['duration']
			ease_type           = own['tween' + number]['ease_type']
			
			obj_prop_on_start       = own['tween' + number]['obj_prop_on_start']
			obj_prop_on_start_value = own['tween' + number]['obj_prop_on_start_value']
			obj_prop_on_end         = own['tween' + number]['obj_prop_on_end']
			obj_prop_on_end_value   = own['tween' + number]['obj_prop_on_end_value']
			
			gd_key_on_start       = own['tween' + number]['gd_key_on_start']
			gd_key_on_start_value = own['tween' + number]['gd_key_on_start_value']
			gd_key_on_end         = own['tween' + number]['gd_key_on_end']
			gd_key_on_end_value   = own['tween' + number]['gd_key_on_end_value']
			
			send_message_on_end = own['tween' + number]['send_message_on_end']
			seg_orden_on_end    = own['tween' + number]['seg_orden_on_end']
			
			timer               = time.time() - own['tween' + number]['timer'] - own['tween' + number]['delay']
			
			finish              = None
			
			# Para que funcione delay
			if timer >= 0:
				texto = ''
				# valor para asignar a propiedad del objeto cuando comienza
				if obj_prop_on_start != None:
					getScene[scene].objects[obj][obj_prop_on_start] = obj_prop_on_start_value
					own['tween' + number]['obj_prop_on_start'] = None
					own['tween' + number]['obj_prop_on_start_value'] = None

				# valor para asignar a propiedad de globalDict cuando comienza
				if gd_key_on_start != None:
					gd[gd_key_on_start] = gd_key_on_start_value
					own['tween' + number]['gd_key_on_start'] = None
					own['tween' + number]['gd_key_on_start_value'] = None
				
				# si finish es un objeto, setea finish[x,y,z] CADA VEZ
				# Esto es por si el objeto esta en movimiento
				# FUNCION OBJ_MOVE Y BONE_MOVE
				if function == 'obj_move' or function == 'bone_move':
					# move
					if loc_obj_target != None:
						finish = list(getScene[scene].objects[loc_obj_target].worldPosition)
					else:
						finish = loc_target
					
					change = ['','','']
					for i in range(3):
						if finish[i] != '':
							change[i] = finish[i] - loc_begin[i]
						
					xyz = ['','','']
					for i in range(3):
						if change[i] != '':
							xyz[i] = tween_eq(ease_type, timer, loc_begin[i], change[i], duration)
						#~ print(xyz)
					
					# termina el tiempo de duracion
					if timer > duration:
						xyz = finish
						#~ print('borra', number)
						del(own['tween' + number])
					
						# sendMessage cuando termina
						if send_message_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**send_message_on_end:', send_message_on_end)
							subject = send_message_on_end[0]
							body = send_message_on_end[1]
							own.sendMessage(subject, body)
							
						# function a ejecutar cuando termina
						if obj_prop_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**obj_prop_on_end:', obj_prop_on_end)
							getScene[scene].objects[obj][obj_prop_on_end] = obj_prop_on_end_value
							
						# function a ejecutar cuando termina
						if gd_key_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**gd_key_on_end:', gd_key_on_end)
							gd[gd_key_on_end] = gd_key_on_end_value
						
						# (MD) segunda orden a fijar cuando comienza
						if seg_orden_on_end != None:
							getScene[scene].objects[obj]['seg_orden_tween' + number] = seg_orden_on_end
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**seg_orden_on_end' + number + ':', seg_orden_on_end, end=' ')
								print('**objeto:', obj)
					
					if function == 'obj_move':
						#~ print(function + '(' + obj + ', ' + str(xyz) + ')')
						#~ eval('tween_' + function + '("' + obj + '", ' + str(xyz) + ')')
						

						eval('tween_' + function + '("' + getScene[scene].name + '", "' + obj + '", ' + str(xyz) + ')')
					elif function == 'bone_move':
						#~ print(function + '(' + obj + ', ' + str(xyz) + ')')
						#~ eval('tween_' + function + '("' + obj + ':' + element[1] + '", ' + str(xyz) + ')')
						eval('tween_' + function + '("' + getScene[scene].name + '", "' + obj + ':' + element[1] + '", ' + str(xyz) + ')')
				
				# OBJ_ROTATE
				elif function == 'obj_rotate':
					if rot_obj_target != None:
						finish = list(getScene[scene].objects[rot_obj_target].worldOrientation.to_euler())
					else:
						finish = rot_target
				
					change = ['','','']
					for i in range(3):
						if finish[i] != '':
							change[i] = finish[i] - rot_begin[i]
						
					xyz = ['','','']
					for i in range(3):
						if change[i] != '':
							xyz[i] = tween_eq(ease_type, timer, rot_begin[i], change[i], duration)
						#~ print(xyz)
					
					# termina el tiempo de duracion
					if timer > duration:
						xyz = finish
						#~ print('borra', number)
						del(own['tween' + number])
					
						# sendMessage cuando termina
						if send_message_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**send_message_on_end:', send_message_on_end)
							subject = send_message_on_end[0]
							body = send_message_on_end[1]
							own.sendMessage(subject, body)
							
						# function a ejecutar cuando termina
						if obj_prop_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**obj_prop_on_end:', obj_prop_on_end)
							getScene[scene].objects[obj][obj_prop_on_end] = obj_prop_on_end_value
					
						# function a ejecutar cuando termina
						if gd_key_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**gd_key_on_end:', gd_key_on_end)
							gd[gd_key_on_end] = gd_key_on_end_value
					
						# (MD) segunda orden a fijar cuando comienza
						if seg_orden_on_end != None:
							getScene[scene].objects[obj]['seg_orden_tween' + number] = seg_orden_on_end
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**seg_orden_on_end' + number + ':', seg_orden_on_end, end=' ')
								print('**objeto:', obj)
					
					#~ print(function + '(' + obj + ', ' + str(xyz) + ')')
					#~ eval('tween_' + function + '("' + obj + '", ' + str(xyz) + ')')
					eval('tween_' + function + '("' + getScene[scene].name + '", "' + obj + '", ' + str(xyz) + ')')
				
				# OBJ_SCALE
				elif function == 'obj_scale':
					if scl_obj_target != None:
						finish = list(getScene[scene].objects[scl_obj_target].worldScale)
					else:
						finish = scl_target
				
					change = ['','','']
					for i in range(3):
						if finish[i] != '':
							change[i] = finish[i] - scl_begin[i]
						
					xyz = ['','','']
					for i in range(3):
						if change[i] != '':
							xyz[i] = tween_eq(ease_type, timer, scl_begin[i], change[i], duration)
						#~ print(xyz)
					
					# termina el tiempo de duracion
					if timer > duration:
						xyz = finish
						#~ print('borra', number)
						del(own['tween' + number])
					
						# sendMessage cuando termina
						if send_message_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**send_message_on_end:', send_message_on_end)
							subject = send_message_on_end[0]
							body = send_message_on_end[1]
							own.sendMessage(subject, body)
							
						# function a ejecutar cuando termina
						if obj_prop_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**obj_prop_on_end:', obj_prop_on_end)
							own[obj_prop_on_end] = obj_prop_on_end_value
					
						# function a ejecutar cuando termina
						if gd_key_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**gd_key_on_end:', gd_key_on_end)
							gd[prop_obj_prop_on_end] = gd_key_on_end_value
					
						# (MD) segunda orden a fijar cuando comienza
						if seg_orden_on_end != None:
							getScene[scene].objects[obj]['seg_orden_tween' + number] = seg_orden_on_end
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**seg_orden_on_end' + number + ':', seg_orden_on_end, end=' ')
								print('**objeto:', obj)
					
					#~ print(function + '(' + obj + ', ' + str(xyz) + ')')
					eval('tween_' + function + '("' + obj + '", ' + str(xyz) + ')')
				
				# FUNCION OBJ_COLOR
				elif function == 'obj_color':
					finish = color
					
					change = ['','','','']
					for i in range(4):
						if finish[i] != '':
							change[i] = finish[i] - color_begin[i]
					
					rgba = ['','','', '']
					for i in range(4):
						if change[i] != '':
							rgba[i] = tween_eq(ease_type, timer, color_begin[i], change[i], duration)
					
					# termina el tiempo de duracion
					if timer > duration:
						rgba = finish
						#~ print('borra', number)
						del(own['tween' + number])
						
						# sendMessage cuando termina
						if send_message_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**send_message_on_end:', send_message_on_end)
							subject = send_message_on_end[0]
							body = send_message_on_end[1]
							own.sendMessage(subject, body)
						
						# function a ejecutar cuando termina
						if obj_prop_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**obj_prop_on_end:', obj_prop_on_end)
							own[obj_prop_on_end] = obj_prop_on_end_value
						
						# function a ejecutar cuando termina
						if gd_key_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**gd_key_on_end:', gd_key_on_end)
							gd[gd_key_on_end] = gd_key_on_end_value
						
						# (MD) segunda orden a fijar cuando comienza
						if seg_orden_on_end != None:
							getScene[scene].objects[obj]['seg_orden_tween' + number] = seg_orden_on_end
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**seg_orden_on_end' + number + ':', seg_orden_on_end, end=' ')
								print('**objeto:', obj)
					
					#~ print('tween_obj_color(' + element + ', ' + str(rgba) + ')')
					#~ eval('tween_obj_color("' + obj + '", ' + str(rgba) + ')')
					eval('tween_obj_color("' + getScene[scene].name + '", "' + obj + '", ' + str(rgba) + ')')
				
				# FUNCION CONSTRAINT ENFORCE
				elif function == 'constraint_enforce':
				
					change = enforce - enforce_begin
					x = tween_eq(ease_type, timer, enforce_begin, change, duration)
					
					# termina el tiempo de duracion
					if timer > duration:
						x = enforce
						#~ print('borra', number)
						del(own['tween' + number])
						
						# sendMessage cuando termina
						if send_message_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**send_message_on_end:', send_message_on_end)
							subject = send_message_on_end[0]
							body = send_message_on_end[1]
							own.sendMessage(subject, body)
							
						# Funcion a ejecutar cuando termina
						if obj_prop_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**obj_prop_on_end:', obj_prop_on_end)
							own[obj_prop_on_end] = obj_prop_on_end_value
					
						# Funcion a ejecutar cuando termina
						if gd_key_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**gd_key_on_end:', gd_key_on_end)
							gd[gd_key_on_end] = gd_key_on_end_value
					
						# (MD) segunda orden a fijar cuando comienza
						if seg_orden_on_end != None:
							getScene[scene].objects[obj]['seg_orden_tween' + number] = seg_orden_on_end
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**seg_orden_on_end' + number + ':', seg_orden_on_end, end=' ')
								print('**objeto:', obj)
					
					#~ print('tween_constraint_enforce(' + element + ', ' + str(x) + ')')
					#~ eval('tween_constraint_enforce("' + obj + ':' + element[1] + ':' + element[2] + '", ' + str(x) + ')')
					eval('tween_constraint_enforce("' + getScene[scene].name + '", "' + obj + ':' + element[1] + ':' + element[2] + '", ' + str(x) + ')')
				
				# FUNCION PROPERTY
				elif function == 'property':
				
					change = prop_value - prop_value_begin
					x = tween_eq(ease_type, timer, prop_value_begin, change, duration)
					
					# termina el tiempo de duracion
					if timer > duration:
						x = prop_value
						#~ print('borra', number)
						del(own['tween' + number])
						
						# sendMessage cuando termina
						if send_message_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**send_message_on_end:', send_message_on_end)
							subject = send_message_on_end[0]
							body = send_message_on_end[1]
							own.sendMessage(subject, body)
							
						# Funcion a ejecutar cuando termina
						if obj_prop_on_end != None:
							own[obj_prop_on_end] = obj_prop_on_end_value
					
						# Funcion a ejecutar cuando termina
						if gd_key_on_end != None:
							gd[gd_key_on_end] = gd_key_on_end_value
					
						# (MD) segunda orden a fijar cuando comienza
						if seg_orden_on_end != None:
							getScene[scene].objects[obj]['seg_orden_tween' + number] = seg_orden_on_end
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**seg_orden_on_end' + number + ':', seg_orden_on_end, end=' ')
								print('**objeto:', obj)
					
					#~ print('tween_constraint_enforce(' + element + ', ' + str(x) + ')')
					#~ eval('tween_obj_property("' + obj + ':' + element[1] + '", ' + str(x) + ')')
					eval('tween_obj_property("' + getScene[scene].name + '", "' + obj + ':' + element[1] + '", ' + str(x) + ')')
				
				#~ # FUNCION ONLYSENDMESSAGE
				#~ elif function == 'onlySendMessage':
					#~ 
					#~ # termina el tiempo de duracion
					#~ if timer > duration:
						#~ print('borra', number)
						#~ del(own['tween' + number])
						#~ 
						#~ # sendMessage cuando termina
						#~ if send_message_on_end != None:
							#~ if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								#~ print('**send_message_on_end:', send_message_on_end)
							#~ subject = send_message_on_end[0]
							#~ body = send_message_on_end[1]
							#~ own.sendMessage(subject, body)
				
				# FUNCION noObjLocRotSclColChange
				elif function == 'noObjLocRotSclColChange':
					if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_obj_no_obj_change:
						print('timer:', timer, 'duration:', duration)
	
					
					# termina el tiempo de duracion
					if timer > duration:
						#~ print('borra', number)
						del(own['tween' + number])
						
						# sendMessage cuando termina
						if send_message_on_end != None:
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**send_message_on_end:', send_message_on_end)
							subject = send_message_on_end[0]
							body = send_message_on_end[1]
							own.sendMessage(subject, body)
							
						# Funcion a ejecutar cuando termina
						if obj_prop_on_end != None:
							own[obj_prop_on_end] = obj_prop_on_end_value
						
						# Funcion a ejecutar cuando termina
						if gd_key_on_end != None:
							gd[gd_key_on_end] = gd_key_on_end_value
						
						# (MD) segunda orden a fijar cuando comienza
						if seg_orden_on_end != None:
							getScene[scene].objects[obj]['seg_orden_tween' + number] = seg_orden_on_end
							if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
								print('**seg_orden_on_end' + number + ':', seg_orden_on_end, end=' ')
								print('**objeto:', obj)


# TWEEN - Ecuaciones
def tween_eq(ease_type, t, b, c, d):
	#~ if t >= 0:
	if ease_type == 'linear':
		return c * t / d + b
	
	elif ease_type == 'inQuad':
		t /= d
		return c * t * t + b
	
	elif ease_type == 'outQuad':
		t /= d
		return - c * t * (t - 2) + b
	
	elif ease_type == 'inOutQuad':
		t /= d / 2
		if (t < 1):
			return c / 2 * t * t + b
		t -= 1
		return -c / 2 * ((t) * (t - 2) - 1) + b
	
	
	elif ease_type == 'inCubic':
		t /= d
		return c * t * t * t + b
	
	elif ease_type == 'outCubic':
		t /= d
		t -= 1
		return c * (t * t * t + 1) + b
	
	elif ease_type == 'inOutCubic':
		t /= d / 2
		if (t < 1):
			return c / 2 * t * t * t + b
		t -= 2
		return c / 2 * (t * t * t + 2) + b
		
	#~ elif ease_type == 'easeOutElastic':
		#~ s=1.70158
		#~ p=0
		#~ a=c
		#~ if t == 0:
			#~ return b
		#~ if t/=d == 1:
			#~ return b+c
		#~ if not p:
			#~ p=d*.3
		#~ if a < Math.abs(c):
			#~ a = c
			#~ s = p/4
		#~ else:
			#~ s=p/(2*Math.PI)*Math.asin(c/a)
		#~ return a*Math.pow(2,-10*t)*Math.sin((t*d-s)*(2*Math.PI)/p)+c+b
		
		#~ https://github.com/danro/jquery-easing/blob/master/jquery.easing.js
		#~ easeOutElastic:function(x,t,b,c,d){
		#~ vars=1.70158;varp=0;vara=c;
		#~ if(t==0)returnb;if((t/=d)==1)returnb+c;if(!p)p=d*.3;
		#~ if(a<Math.abs(c)){a=c;vars=p/4;}
		#~ elsevars=p/(2*Math.PI)*Math.asin(c/a);
		#~ returna*Math.pow(2,-10*t)*Math.sin((t*d-s)*(2*Math.PI)/p)+c+b;
		#~ },

# recibe objeto y valor en lista[x,y,z]
def tween_obj_move(scene, element, xyz):
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_obj_move:
		print('tween_obj_move(' + element, str(xyz) + ')')
	
	for i in range(3):
		if xyz[i] != '':
			getScene[scene].objects[element].worldPosition[i] = xyz[i]
		

# recibe objeto y valor euler en lista[x,y,z]
def tween_obj_rotate(scene, element, xyz):
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_obj_rotate:
		print('tween_obj_rotate(' + element, str(xyz) + ')')

	new_euler = getScene[scene].objects[element].worldOrientation.to_euler()

	for i in range(3):
		if xyz[i] != '': new_euler[i] = xyz[i]
			
	getScene[scene].objects[element].worldOrientation = new_euler.to_matrix()

# recibe objeto y valor en lista[x,y,z]
def tween_obj_scale(scene, element, xyz):
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_obj_scale:
		print('tween_obj_scale(' + element, str(xyz) + ')')
	
	for i in range(3):
		if xyz[i] != '': getScene[scene].objects[element].localScale[i] = xyz[i]

# recibe objeto:property y el valor de property
def tween_obj_property(scene, element, x):
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_obj_property:
		print('tween_obj_property(' + element, str(x) + ')')
	
	element = element.split(':')
	getScene[scene].objects[element[0]][element[1]] = x

# recibe objeto y valor en lista[r,g,b,a]
def tween_obj_color(scene, element, rgba):
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_obj_color:
		print('tween_obj_color(' + element, str(rgba) + ')')

	for i in range(4):
		if rgba[i] != '': getScene[scene].objects[element].color[i] = rgba[i]

# recibe objeto y valor en lista[r,g,b,a]
# TO-DO
def tween_obj_diff_color(scene, element, rgba):
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_obj_diff_color:
		print('tween_obj_diff_color(' + element, str(rgba) + ')')

	for i in range(4):
		if rgba[i] != '': getScene[scene].objects[element].color[i] = rgba[i]

# recibe objeto:bone y valor en lista[x,y,z]
def tween_bone_move(scene, element, xyz):
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_bone_move:
		print('tween_bone_move(' + element, str(xyz) + ')')
	
	element = element.split(':')
	new_vector = getScene[scene].objects[element[0]].channels[element[1]].location
	
	for i in range(3):
		if xyz[i] != '': new_vector[i] = xyz[i]
	
	getScene[scene].objects[element[0]].channels[element[1]].location = new_vector

# recibe objeto:bone:constraint y el valor de enforce
def tween_constraint_enforce(scene, element, x):
	if 'print_tween_funciones' in gd and gd['print_tween_funciones'] and print_constraint_enforce:
		print('tween_constraint_enforce(' + element, str(x) + ')')
	
	element = element.split(':')
	getScene[scene].objects[element[0]].constraints[element[1] + ':' + element[2]].enforce = x

# Tween para importar en main y md
def tween_evento(evento):
	# claves y valores por defecto
	_scene = current_scene.name
	_element = own.name
	
	_enforce_begin = None
	_enforce = None
	_color_begin = None
	_color = None
	
	_loc_obj_begin = None
	_loc_begin = None
	_loc_obj_target = None
	_loc_target = None
	
	_rot_obj_begin = None
	_rot_begin = None
	_rot_obj_target = None
	_rot_target = None
	
	_scl_obj_begin = None
	_scl_begin = None
	_scl_obj_target = None
	_scl_target = None
	
	_delay = 0
	_duration = 1.0
	_ease_type = 'outQuad'
	
	_obj_prop_on_start = None
	_obj_prop_on_start_value = None
	_obj_prop_on_end = None
	_obj_prop_on_end_value = None
	
	_gd_key_on_start = None
	_gd_key_on_start_value = None
	_gd_key_on_end = None
	_gd_key_on_end_value = None
	
	_send_message_on_end = None
	_seg_orden_on_end = None
	
	if 'scene' in evento:               _scene                  = evento['scene']
	if 'element' in evento:             _element                = evento['element']
	
	if 'enforce_begin' in evento:       _enforce_begin          = evento['enforce_begin']
	if 'enforce' in evento:             _enforce                = evento['enforce']
	if 'color_begin' in evento:         _color_begin            = evento['color_begin']
	if 'color' in evento:               _color                  = evento['color']
	
	if 'loc_obj_begin' in evento:       _loc_obj_begin          = evento['loc_obj_begin']
	if 'loc_begin' in evento:           _loc_begin              = evento['loc_begin']
	if 'loc_obj_target' in evento:      _loc_obj_target         = evento['loc_obj_target']
	if 'loc_target' in evento:          _loc_target             = evento['loc_target']
	
	if 'rot_obj_begin' in evento:       _rot_obj_begin          = evento['rot_obj_begin']
	if 'rot_begin' in evento:           _rot_begin              = evento['rot_begin']
	if 'rot_obj_target' in evento:      _rot_obj_target         = evento['rot_obj_target']
	if 'rot_target' in evento:          _rot_target             = evento['rot_target']
	
	if 'scl_obj_begin' in evento:       _scl_obj_begin          = evento['scl_obj_begin']
	if 'scl_begin' in evento:           _scl_begin              = evento['scl_begin']
	if 'scl_obj_target' in evento:      _scl_obj_target         = evento['scl_obj_target']
	if 'scl_target' in evento:          _scl_target             = evento['scl_target']
	
	if 'delay' in evento:               _delay                  = evento['delay']
	if 'duration' in evento:            _duration               = evento['duration']
	if 'ease_type' in evento:           _ease_type              = evento['ease_type']
	
	if 'obj_prop_on_start' in evento:       _obj_prop_on_start          = evento['obj_prop_on_start']
	if 'obj_prop_on_start_value' in evento: _obj_prop_on_start_value    = evento['obj_prop_on_start_value']
	if 'obj_prop_on_end' in evento:         _obj_prop_on_end            = evento['obj_prop_on_end']
	if 'obj_prop_on_end_value' in evento:   _obj_prop_on_end_value      = evento['obj_prop_on_end_value']
	
	if 'gd_key_on_start' in evento:       _gd_key_on_start          = evento['gd_key_on_start']
	if 'gd_key_on_start_value' in evento: _gd_key_on_start_value    = evento['gd_key_on_start_value']
	if 'gd_key_on_end' in evento:         _gd_key_on_end            = evento['gd_key_on_end']
	if 'gd_key_on_end_value' in evento:   _gd_key_on_end_value      = evento['gd_key_on_end_value']
	
	if 'seg_orden_on_end' in evento:    _seg_orden_on_end       = evento['seg_orden_on_end']
	if 'send_message_on_end' in evento:    _send_message_on_end       = evento['send_message_on_end']
	
	tween(		scene = _scene,
				element = _element,
				
				enforce_begin = _enforce_begin, 
				enforce = _enforce, 
				color_begin = _color_begin, 
				color = _color,
				
				loc_begin = _loc_begin,
				loc_target = _loc_target,
				loc_obj_begin = _loc_obj_begin, 
				loc_obj_target = _loc_obj_target, 
				
				rot_begin = _rot_begin,
				rot_target = _rot_target,
				rot_obj_begin = _rot_obj_begin, 
				rot_obj_target = _rot_obj_target, 
				
				scl_begin = _scl_begin,
				scl_target = _scl_target,
				scl_obj_begin = _scl_obj_begin, 
				scl_obj_target = _scl_obj_target, 
				
				delay = _delay, 
				duration = _duration, 
				ease_type = _ease_type,
				
				obj_prop_on_start = _obj_prop_on_start,
				obj_prop_on_start_value = _obj_prop_on_start_value,
				obj_prop_on_end = _obj_prop_on_end,
				obj_prop_on_end_value = _obj_prop_on_end_value,
				
				gd_key_on_start = _gd_key_on_start,
				gd_key_on_start_value = _gd_key_on_start_value,
				gd_key_on_end = _gd_key_on_end,
				gd_key_on_end_value = _gd_key_on_end_value,
				
				send_message_on_end = _send_message_on_end,
				seg_orden_on_end = _seg_orden_on_end)
