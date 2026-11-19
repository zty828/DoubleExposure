import unreal,json
L=unreal.MaterialEditingLibrary
m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile')
m.modify()
ex={str(e.get_editor_property('parameter_name')):e for e in L.get_material_expressions(m) if isinstance(e,(unreal.MaterialExpressionScalarParameter,unreal.MaterialExpressionVectorParameter))}
expected=['TilingA','TilingB','WeightA','WeightB','NormalStrength','FlowSpeed','ShallowColor','DeepColor','Roughness','Specular']
missing=[n for n in expected if n not in ex]
assert not missing,missing
# Keep broad organic motion, restore moderate smaller-scale secondary ripples.
for name,value in {'TilingA':0.85,'TilingB':1.65,'WeightA':0.8,'WeightB':0.42,'NormalStrength':0.72,'FlowSpeed':0.07,'Roughness':0.055,'Specular':0.225}.items():
 ex[name].set_editor_property('default_value',float(value))
# Lift the body colour toward sky cyan without emissive or Fresnel colour paint.
ex['ShallowColor'].set_editor_property('default_value',unreal.LinearColor(0.10,0.38,0.44,1.0))
ex['DeepColor'].set_editor_property('default_value',unreal.LinearColor(0.035,0.19,0.26,1.0))
for name,desc in {'TilingB':'Secondary organic ripples; moderate scale, below v3 high-frequency tiling.','WeightB':'Visible small cross-flow, below v3 WeightC=1.0.','ShallowColor':'Sky-cyan body colour; no emissive term.','DeepColor':'Lifted cyan depth colour, not navy.'}.items():ex[name].set_editor_property('desc',desc)
warnings=list(L.recompile_material(m))
errors=[e.get_name() for e in L.get_material_error_expressions(m) if e]
assert not errors,errors
L.layout_material_expressions(m)
unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
mi=unreal.load_asset('/Game/DoubleExposure/Materials/MI_River.MI_River')
assert mi.get_editor_property('parent')==m
json.dumps({'saved':m.get_path_name(),'instance':mi.get_path_name(),'warnings':[str(x) for x in warnings],'errors':errors,'parameters':{name:str(ex[name].get_editor_property('default_value')) for name in expected},'stats':str(L.get_statistics(m))})
