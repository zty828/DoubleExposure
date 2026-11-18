import unreal,json
L=unreal.MaterialEditingLibrary;m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile')
ex={e.get_name():e for e in L.get_material_expressions(m)}
out={'errors':[e.get_name() for e in L.get_material_error_expressions(m)],'stats':str(L.get_statistics(m)),'shader_count':L.get_num_shader_types(m),'used_textures':[t.get_path_name() for t in L.get_used_textures(m)],'opacity':{},'normal':{},'instance':{}}
for p in ['OPACITY','NORMAL']:
 n=L.get_material_property_input_node(m,getattr(unreal.MaterialProperty,'MP_'+p));out[p.lower()]=n.get_name() if n else None
mi=unreal.load_asset('/Game/DoubleExposure/Materials/MI_River.MI_River')
for n in ['NormalStrength','Opacity','Roughness','FlowSpeed']:
 out['instance'][n]=L.get_material_instance_scalar_parameter_value(mi,n)
json.dumps(out)