import unreal,json
L=unreal.MaterialEditingLibrary
m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile')
mi=unreal.load_asset('/Game/DoubleExposure/Materials/MI_River.MI_River')
ex=L.get_material_expressions(m)
json.dumps({'loaded':m.get_path_name(),'parent':mi.get_editor_property('parent').get_path_name(),'preview':str(unreal.EditorSubsystemBlueprintLibrary.get_preview_platform_name()),'params':{str(e.get_editor_property('parameter_name')):e.get_editor_property('default_value') for e in ex if isinstance(e,unreal.MaterialExpressionScalarParameter)},'textures':[t.get_path_name() for t in L.get_used_textures(m)],'stats':str(L.get_statistics(m)),'errors':[str(x) for x in L.recompile_material(m)]})