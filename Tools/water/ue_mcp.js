// Minimal UE 5.9 built-in MCP JSON-RPC client for water-material work.
const fs = require('fs');
const BASE='http://127.0.0.1:8000/mcp';
let sid=null, id=0;
async function rpc(method,params){
  const headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream'};
  if(sid) headers['Mcp-Session-Id']=sid;
  const res=await fetch(BASE,{method:'POST',headers,body:JSON.stringify({jsonrpc:'2.0',...(method.startsWith('notifications/')?{}:{id:++id}),method,params})});
  if(res.headers.get('mcp-session-id')) sid=res.headers.get('mcp-session-id');
  const text=await res.text();
  if(method.startsWith('notifications/')) return null;
  const lines=text.split(/\r?\n/).filter(l=>l.startsWith('data:'));
  const payload=lines.length?lines.map(l=>l.slice(5).trim()).join(''):text;
  return JSON.parse(payload);
}
(async()=>{
  await rpc('initialize',{protocolVersion:'2025-06-18',capabilities:{},clientInfo:{name:'water-v4',version:'1.0'}});
  await rpc('notifications/initialized',{});
  const mode=process.argv[2];
  let resp;
  if(mode==='describe') resp=await rpc('tools/call',{name:'describe_toolsets',arguments:{toolset_names:[process.argv[3]]}});
  else if(mode==='call') resp=await rpc('tools/call',{name:'call_tool',arguments:JSON.parse(fs.readFileSync(process.argv[3],'utf8'))});
  else if(mode==='python') resp=await rpc('tools/call',{name:'call_tool',arguments:{toolset_name:'editor_toolset.toolsets.python_scripting.PythonScriptingTools',tool_name:'execute_python',arguments:{script:{content:fs.readFileSync(process.argv[3],'utf8'),language:'Python'}}}});
  else throw new Error('Usage: node ue_mcp.js describe TOOLSET | call JSON | python SCRIPT');
  const content=(resp.result&&resp.result.content)||[];
  const text=content.filter(x=>x.type==='text').map(x=>x.text).join('\n');
  console.log(text||JSON.stringify(resp,null,2));
  const images=content.filter(x=>x.type==='image');
  for(let i=0;i<images.length;i++){const p=process.argv[4]||`F:/CG/Projects/PICOUE/logs/water-assets/mcp-${Date.now()}-${i}.png`;fs.writeFileSync(p,Buffer.from(images[i].data,'base64'));console.log('IMAGE '+p+' '+fs.statSync(p).size);}
})().catch(e=>{console.error(e);process.exit(1)});
