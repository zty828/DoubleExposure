import unreal,json
L=unreal.MaterialEditingLibrary
m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile')
m.modify()
nodes=L.get_material_expressions(m)
ex={e.get_name():e for e in nodes}
params={str(e.get_editor_property('parameter_name')):e for e in nodes if isinstance(e,(unreal.MaterialExpressionScalarParameter,unreal.MaterialExpressionVectorParameter))}
assert 'WaterScale' not in params,'Run once on v5; use finalize_v6.py for subsequent tuning.'
# Match the Water plugin's world-space mapping: WorldPosition XY / centimetres per tile.
wp=L.create_material_expression(m,unreal.MaterialExpressionWorldPosition,-1000,-900)
wp.set_editor_property('desc','World-space water mapping: object scale cannot stretch ripple density.')
mask=L.create_material_expression(m,unreal.MaterialExpressionComponentMask,-800,-900)
mask.set_editor_property('r',True);mask.set_editor_property('g',True);mask.set_editor_property('b',False);mask.set_editor_property('a',False)
scale=L.create_material_expression(m,unreal.MaterialExpressionScalarParameter,-800,-680)
scale.set_editor_property('parameter_name','WaterScale');scale.set_editor_property('default_value',1536.0)
scale.set_editor_property('group','River · Mobile VR')
scale.set_editor_property('desc','World-space centimetres per repeat; object scale cannot change ripple density.')
div=L.create_material_expression(m,unreal.MaterialExpressionDivide,-560,-820)
for src,dst,pin in [(wp,mask,'Input'),(mask,div,'A'),(scale,div,'B'),(div,ex['MaterialExpressionMultiply_19'],'A'),(div,ex['MaterialExpressionMultiply_22'],'A')]:
 assert L.connect_material_expressions(src,'',dst,pin),(src.get_name(),dst.get_name(),pin)
params['ShallowColor'].set_editor_property('default_value',unreal.LinearColor(0.14,0.48,0.54,1.0))
params['DeepColor'].set_editor_property('default_value',unreal.LinearColor(0.07,0.30,0.35,1.0))
params['ShallowColor'].set_editor_property('desc','Bright sky-cyan body colour, balanced green/blue without emissive.')
params['DeepColor'].set_editor_property('desc','Cyan-teal depth colour, no navy-blue base.')
params['TilingA'].set_editor_property('desc','Relative world tiling; finalizer tunes appearance.')
params['TilingB'].set_editor_property('desc','Relative world tiling; finalizer tunes appearance.')
for name in ['MaterialExpressionTextureCoordinate_6','MaterialExpressionTextureCoordinate_7']:
 assert ex[name] in nodes
 L.delete_material_expression(m,ex[name])
warnings=list(L.recompile_material(m))
errors=[e.get_name() for e in L.get_material_error_expressions(m) if e]
assert not errors,errors
unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
mi=unreal.load_asset('/Game/DoubleExposure/Materials/MI_River.MI_River')
assert mi.get_editor_property('parent')==m
out={'saved':m.get_path_name(),'water_scale_cm':1536.0,'broad_repeat_cm':1536.0/.85,'secondary_repeat_cm':1536.0/1.65,'colors':[str(params[n].get_editor_property('default_value')) for n in ['ShallowColor','DeepColor']],'warnings':[str(x) for x in warnings],'errors':errors,'stats':str(L.get_statistics(m)),'texcoord_nodes':[e.get_name() for e in L.get_material_expressions(m) if isinstance(e,unreal.MaterialExpressionTextureCoordinate)],'world_mapping':{'world_position':wp.get_name(),'xy_mask':mask.get_name(),'divide':div.get_name(),'scale':scale.get_name()}}
json.dumps(out)