import unreal,json
p=unreal.EditorSubsystemBlueprintLibrary;m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile')
json.dumps({'platform':str(p.get_preview_platform_name()),'warnings':[str(x) for x in unreal.MaterialEditingLibrary.recompile_material(m)],'stats':str(unreal.MaterialEditingLibrary.get_statistics(m))})