import json
import math
world = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()[0].get_world()
landscape = next(a for a in actors if isinstance(a, unreal.Landscape)) if (actors := unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()) else None
points = []
for y in range(-11000, 11001, 1000):
    for x in range(-12000, 12001, 1000):
        start = unreal.Vector(x,y,15000)
        end = unreal.Vector(x,y,-15000)
        hit = unreal.SystemLibrary.line_trace_single(world,start,end,unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[landscape],unreal.DrawDebugTrace.NONE,False)
        if hit:
            points.append({'x':x,'y':y,'z':round(hit.impact_point.z,2),'actor':hit.get_hit_actor().get_name()})
summary={'count':len(points),'z_min':min(p['z'] for p in points),'z_max':max(p['z'] for p in points),'lowest':sorted(points,key=lambda p:p['z'])[:80]}
json.dumps(summary)
