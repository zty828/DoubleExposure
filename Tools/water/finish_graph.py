import unreal,json
L=unreal.MaterialEditingLibrary;m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile');m.modify()
for e in L.get_material_expressions(m):
 if hasattr(e,'parameter_name') and str(e.get_editor_property('parameter_name'))!='None':e.set_editor_property('group',unreal.Name('River · Mobile VR'))
ex={e.get_name():e for e in L.get_material_expressions(m)}
ex['MaterialExpressionScalarParameter_35'].set_editor_property('desc','Weak cross-flow; broad A layer dominates. Reference: Water Near Normal Strength .25.')
ex['MaterialExpressionConstant_17'].set_editor_property('desc','Fresnel sky tint multiplier: 0 disables opaque-looking cyan veil. Reflections remain physical.')
ex['MaterialExpressionConstant_18'].set_editor_property('desc','Shore fade enabled: multiply opacity by soft shore depth fade.')
ex['MaterialExpressionFresnel_2'].set_editor_property('desc','Mobile approximation of Water Fresnel; exponent 5, base reflect .02.')
w=L.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
unreal.EditorSubsystemBlueprintLibrary.disable_preview_platform()
json.dumps({'warnings':[str(x) for x in w],'preview':str(unreal.EditorSubsystemBlueprintLibrary.get_preview_platform_name()),'errors':[e.get_name() if e else None for e in L.get_material_error_expressions(m)]})