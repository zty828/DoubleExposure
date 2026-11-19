import unreal,json
L=unreal.MaterialEditingLibrary;m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile');m.modify()
es=L.get_material_expressions(m);p={str(e.get_editor_property('parameter_name')):e for e in es if isinstance(e,(unreal.MaterialExpressionScalarParameter,unreal.MaterialExpressionVectorParameter))}
for n,v in {'WaterScale':1536.0,'Roughness':0.10,'Specular':0.10,'NormalStrength':0.30,'WeightA':0.70,'WeightB':0.35}.items():p[n].set_editor_property('default_value',v)
p['ShallowColor'].set_editor_property('default_value',unreal.LinearColor(0.18,0.55,0.58,1))
p['DeepColor'].set_editor_property('default_value',unreal.LinearColor(0.10,0.38,0.40,1))
p['WaterScale'].set_editor_property('desc','World centimetres per repeat before TilingA/B. Object scale does not affect ripple density. Water plugin reference uses this mapping.')
p['TilingA'].set_editor_property('desc','Relative world tiling A. At WaterScale=1536, one repeat is about 18.07 m.')
p['TilingB'].set_editor_property('desc','Relative world tiling B. At WaterScale=1536, one repeat is about 9.31 m.')
p['NormalStrength'].set_editor_property('desc','Low combined normal amplitude to suppress large specular white patches at landscape scale.')
p['Specular'].set_editor_property('desc','Controlled mobile specular response, below Water plugin reference .225 to avoid glitter with this sky.')
tex=[e for e in es if isinstance(e,unreal.MaterialExpressionTextureSampleParameter2D)]
uv=[e for e in es if isinstance(e,unreal.MaterialExpressionTextureCoordinate)]
assert not uv,[e.get_name() for e in uv]
assert len(tex)==2,len(tex)
assert all(e.get_editor_property('texture').get_path_name()=='/Game/DoubleExposure/Materials/Textures/T_RiverDetail_Normal.T_RiverDetail_Normal' for e in tex)
wp=[e for e in es if isinstance(e,unreal.MaterialExpressionWorldPosition)]
assert len(wp)==1
pans=[e for e in es if isinstance(e,unreal.MaterialExpressionPanner)]
def ancestors(e):
 out=[];seen=set()
 def walk(n):
  if not n or n.get_name() in seen:return
  seen.add(n.get_name());out.append(n)
  for x in L.get_inputs_for_material_expression(m,n):walk(x)
 walk(e);return out
for pan in pans:
 chain=ancestors(pan)
 assert wp[0] in chain,pan.get_name()
 assert p['WaterScale'] in chain,pan.get_name()
 assert not any(isinstance(x,unreal.MaterialExpressionTextureCoordinate) for x in chain)
mi=unreal.load_asset('/Game/DoubleExposure/Materials/MI_River.MI_River');assert mi.get_editor_property('parent')==m
assert not any('Tiling' in str(x.parameter_info.name) or 'WaterScale' in str(x.parameter_info.name) for x in mi.get_editor_property('scalar_parameter_values'))
L.layout_material_expressions(m)
w=list(L.recompile_material(m));errors=[e.get_name() for e in L.get_material_error_expressions(m) if e]
assert not errors,errors
unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
out={'saved':m.get_path_name(),'instance_parent':mi.get_editor_property('parent').get_path_name(),'water_scale_cm':p['WaterScale'].get_editor_property('default_value'),'repeat_a_m':p['WaterScale'].get_editor_property('default_value')/p['TilingA'].get_editor_property('default_value')/100.0,'repeat_b_m':p['WaterScale'].get_editor_property('default_value')/p['TilingB'].get_editor_property('default_value')/100.0,'flow_speed':p['FlowSpeed'].get_editor_property('default_value'),'normal_strength':p['NormalStrength'].get_editor_property('default_value'),'weights':[p['WeightA'].get_editor_property('default_value'),p['WeightB'].get_editor_property('default_value')],'roughness':p['Roughness'].get_editor_property('default_value'),'specular':p['Specular'].get_editor_property('default_value'),'shallow':str(p['ShallowColor'].get_editor_property('default_value')),'deep':str(p['DeepColor'].get_editor_property('default_value')),'texture_nodes':len(tex),'unique_normal_textures':sorted(set(e.get_editor_property('texture').get_path_name() for e in tex)),'texcoord_nodes':len(uv),'both_panners_world_position_verified':True,'warnings':[str(x) for x in w],'errors':errors,'stats':str(L.get_statistics(m)),'preview':str(unreal.EditorSubsystemBlueprintLibrary.get_preview_platform_name())}
json.dumps(out)