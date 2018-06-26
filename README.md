Tween for BGE, v0.93
===================

tween para BGE, v0.92
Mario Mey - http://www.mariomey.com.ar

Funcion Tween, para (entre otras cosas):

  - mover, rotar, escalar objetos
  - cambiar color, alpha de un objeto
  - cambiar valores de las "properties" de un objeto
  - mover bones
  - cambiar influence de Constraints un bone

...en un tiempo determinado, con un delay para el comienzo, 
usando diferentes equaciones para la interpolacion, etc, etc.


Based in [Tweener](https://code.google.com/p/tweener/), for ActionScript 2 and 3.

Using [Robert Penner's Easing Functions](http://www.robertpenner.com/easing/)


COMPLETE
--------

```
tween.tween(element = own.name, 
duration = 1.0, delay = 0, ease_type = 'outQuad', 
enforce_begin = None, enforce = None, 
color_begin = None, color = None, 
loc_begin = None, loc_target = None, 
loc_obj_begin = None, loc_obj_target = None,
rot_begin = None, rot_target = None, 
rot_obj_begin = None, rot_obj_target = None, 
scl_begin = None, scl_target = None, 
scl_obj_begin = None, scl_obj_target = None, 
obj_prop_on_start = None, obj_prop_on_start_value = None,
obj_prop_on_end = None, obj_prop_on_end_value = None,
gd_key_on_start = None, gd_key_on_start_value = None,
gd_key_on_end = None, gd_key_on_end_value = None,
send_message_on_end = None,
seg_orden_on_end = None)
```

For moving or rotating (euler) or scale object from:
-actual position or 
-[x,y,z] or 
-an object position/rotation/scale.
to:
-[x,y,z] or
-['',y,''] (just Y axis, for example) or
-an object position/rotation/scale.

E.G:
tween.tween(element='Torus', loc_obj_target='Empty.003', duration=3.5, ease_type='linear')
tween.tween(loc_target=['',4,''], obj_prop_on_end='fx', obj_prop_on_end_value=False)
tween.tween(rot_obj_target='Empty.000')
tween.tween(scl_obj=[1,1.5,''])


In Local, for moving bones from:
-actual position or
-[x,y,z] (in local)
to:
-[x,y,z] (in local)
-['',y,''] (just Y axis, for example)

EG: tween.tween(element='Armature:Bone.001', loc_target=[-2,1,2], duration=4)


For changing object color from:
-actual color or
-[r,g,b,a]
to:
-[r,g,b,a] or
-['',g,'',a] (just green and alpha, for example)

EG: tween.tween(element='Suzanne', color=['','','',1], ease_type='inOutQuad')


For changing bone constraint influence from:
-actual influence value
-Float number (0-1)
to:
-Float number (0-1)

EG: tween.tween(element='Armature.001:Bone.001:damp', enforce=1)


Just for sending a message after 1 second:

EG: tween.tween(send_message_on_end=['subj', 'body'])

Defaults
--------

function = ''
element = own.name            ; Name of the object as 'object'
                              ; Name of the bone as 'object:bone'
                              ; Name of the constraint as 'object:bone:constraint'
                              ; Name of an object property as 'object:property'
                              ; Name of own object property as 'property'

prop_value_begin = None       ; Start value of the transition of a object property value (optional)
prop_value = None             ; Final value of the transition of a object property value

enforce_begin = None          ; Start value of the transition of a constraint influence (optional)
enforce = None                ; Final value of the transition of a constraint influence

color_begin = None            ; Start value of the transition of an object color as [r,g,b,a] (optional)
color = None                  ; Final value of the transition of an object color as [r,g,b,a]

loc_obj_begin = None          ; Object (name) to get the starting position for the move transition
loc_begin = None              ; [x,y,z] or ['',5,0.5] of the starting position for the move transition
loc_obj_target = None         ; Object (name) to get the final position for the move transition
loc_target = None             ; [x,y,z] or ['',5,0.5] of the final position for the move transition

rot_obj_begin = None          ; Object (name) to get the starting rotation for the move transition
rot_begin = None              ; [x,y,z] or ['',5,0.5] of the starting rotation for the move transition
rot_obj_target = None         ; Object (name) to get the final rotation for the move transition
rot_target = None             ; [x,y,z] or ['',5,0.5] of the final rotation for the move transition

scl_obj_begin = None          ; Object (name) to get the starting scale for the move transition
scl_begin = None              ; [x,y,z] or ['',5,0.5] of the starting scale for the move transition
scl_obj_target = None         ; Object (name) to get the final scale for the move transition
scl_target = None             ; [x,y,z] or ['',5,0.5] of the final scale for the move transition

delay = 0                     ; Delay before tweening (in seconds)
duration = 1.0                ; Duration of the tweening (in seconds)
ease_type = 'outQuad'         ; Ease type: 'linear', 'outQuad', 'inQuad', 'inOutQuad',
                              ;             'inCubic', 'outCubic' and 'inOutCubic' (Robbert Penner)

obj_prop_on_start = None          ; Own object property (key of object dictionary) to change on tween start
obj_prop_on_start_value = None    ; New value of the property

obj_prop_on_end = None            ; Own object property (key of object dictionary) to change on tween finish
obj_prop_on_end_value = None      ; New value of the property

gd_key_on_start = None            ; globalDict key to change on tween start
gd_key_on_start_value = None      ; New value of the property

gd_key_on_end = None              ; globalDict key to change on tween finish
gd_key_on_end_value = None        ; New value of the property

send_message_on_end = None        ; Send Message when tween ends
seg_orden_on_end = None           ; Second order (to do when tween ends, saved in
								    scene.objects[obj][seg_orden_tween + number], to use with MD)

Based in Tweener, for ActionScript 2 and 3.
https://code.google.com/p/tweener/

Using Robert Penner's Easing Functions
http://www.robertpenner.com/easing/

Mario Mey
http://www.mariomey.com.ar

Changelog:
----------

v0.93 - 20/07/2017:
- tween_evento(). Si no se incluia "element", quedaba en None, en lugar de own.name

v0.92 - 01/07/2016:
- Arreglado para solo enviar mensaje o setear una segunda orden

v0.91 - 26/04/2016:
- Se agrega un mensaje de error si algun objeto usado como referencia no existe.

v0.9 - 18/11/2015:
- Se agrega 'send_message_on_end' para enviar un mensaje cuando termina el tween.
  Acepta que solo envie un mensaje, sin ningun otro tween. 

v0.8 - 17/7/2015:
- Se agregan 'inCubic', 'outCubic' y 'inOutCubic', como equaciones


v0.7 - 17/7/2015:
- Se agrega "print_*", que imprime los cambios en las funciones finales
- Se arregla algunas cosas de "print_tween_funciones"


v0.6 - 16/4/2015:
- 'own_' is replaced by 'obj_' in arguments, to change object properties
- Bugfix: when Tween ends, obj_prop_on_end, gd_key_on_end and seg_orden_tween
  are printed 
- Bugfix: some 'own' variables changed to 'obj' to control properties
  of an object that it is not own
- Bugfix: seg_orden_tween fixed
- For example: if loc_begin == loc_target, the operation is cancelled

- Se cambia 'own_' por 'obj_', por las properties del objeto en cuestion.
- Bugfix: Cuando termina Tween, obj_prop_on_end, gd_key_on_end and seg_orden_tween
  se imprimen en la consola.
- Bugfix: algunas variables 'own' cambiaron a 'obj' para controlar las
  properties del objeto que no es own
- Bugfix: seg_orden_tween arreglado
- Por ejemplo: si loc_begin == loc_target, la operacion es cancelada

v0.5 - 2/4/2015:
- prop_on_start, prop_on_start_value, prop_on_end, prop_on_end_value
  are now own_prop_on_start, own_prop_on_start_value,
  own_prop_on_end and own_prop_on_end_value
  
- gd_key_on_start, gd_key_on_start_value, 
  gd_key_on_end, gd_key_on_end_value
  It works the same as with own_prop_on_start, etc, but using globalDict

v0.4 - 26/11/2014:
- prop_value, prop_value_begin:
  It works the same as with Enforce, using object's property
  'element' must be 'object:property' or just 'property' (own object)
  Funciona igual que con Enforce, usando una property del objeto
  'element' puede ser 'object:property' o solo 'property' (objecto own)

v0.3 - 23/10/2014:
- scl_obj_begin, scl_begin, scl_obj_target, scl_target:
  It works the same as with Position
  Funciona igual que con Position


v0.2 - 22/10/2014:
- own_prop_on_start, own_prop_on_start_value:
  Value assing to an object property on tween start
  Asignacion de un valor a una propiedad de un objeto cuando comienza el tween.

- seg_orden_on_end:
  Second Order, Tween version (MD component)
  Segunda Orden, version Tween (componente de las MD)

- delay:
  Delay before tween starting.
  Delay antes de comenzar el tween.

- rot_obj_begin, rot_begin, rot_obj_target, rot_target:
  It works the same as with Position
  Funciona igual que con Position


v0.1 – 1/10/2014:
- Only 1 or 2 axis bone movement fixed.
- Solucionado el movimiento de bones en 1 o 2 ejes solamente.

vSinNumero – 20/8/2014
- Lanzamiento inicial
- Initial launch
