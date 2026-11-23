import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { stripTypeScriptTypes } from 'node:module';
import { runInNewContext } from 'node:vm';
// Read-only isolated replay of pinned source. No fetch, install or product startup.
const root = process.argv[2];
if (!root) throw new Error('Usage: node replay_cases.mjs /path/to/sciencediscovery-checkout');
const get=(commit,path)=>execFileSync('git',['-C',root,'show',`${commit}:${path}`],{encoding:'utf8'});
const clean=(src)=>stripTypeScriptTypes(src.replace(/^import\s[\s\S]*?;\r?\n/gm,'').replace(/^export /gm,''),{mode:'transform'});
const cases=[];
for(const [stage,commit] of [['before','af8f0736c01116cd256925455f7fab330c6df4e2'],['fixed','31f724fae4843ec7c4508e5f2caf02640cad6f6e']]){
  const bounded=get(commit,'packages/tools/src/bounded-output.ts');
  const filepage=get(commit,'packages/workspace/src/file-page.ts');
  const binary=filepage.slice(filepage.indexOf('export function isBinaryContent('),filepage.indexOf('export async function detectBinaryFile('));
  assert(binary.includes('return true;'));
  const projection=get(commit,'packages/workspace/src/artifact-read.ts');
  const context={Buffer,TextDecoder};
  runInNewContext(clean(bounded)+'\n'+clean(binary)+'\n'+clean(projection)+'\nglobalThis.replay=projectArtifactContent;',context);
  const bytes=Buffer.from(`${'x'.repeat(999)}\n`.repeat(9500),'utf8');
  const outcomes=[];
  for(const offset of [8389,8390,8394,11500]){
    const result=context.replay(bytes,'text/csv',{limit:40,offset});
    assert.equal(result.truncated,true);
    assert.equal(result.page.totalLines,8389);
    if(stage==='before'){
      assert.equal(result.page.hasMore,true);
      assert.equal(result.page.nextOffset,offset===8389 ? 8390 : offset);
    }else{
      assert.equal(result.page.hasMore,false);
      assert.equal(Object.hasOwn(result.page,'nextOffset'),false);
      assert.match(result.note,/offset cannot reach past line 8389/);
    }
    outcomes.push({offset,hasMore:result.page.hasMore,nextOffset:result.page.nextOffset??null,contentBytes:Buffer.byteLength(result.content)});
  }
  cases.push({id:`artifact-pagination-${stage}`,outcome:stage==='before'?'defect-present':'specific-defect-absent',checks:outcomes});
}
for(const [stage,commit] of [['before','60626de259d947a552df54cbdd31f8821ac33dcc'],['fixed','070e90cc737c76b2a3c91d46d41e2404ac681543']]){
  const source=get(commit,'services/api/src/agent-run/versioning-authorities.ts');
  const context={CasStore:class{constructor(){} async retain(ref,pool){return {ref,pool};}}};
  runInNewContext(clean(source)+'\nglobalThis.replay=versioningAuthorities;',context);
  const owners=['main','subagent:child','subagent:sibling'];
  const snapshot=(sessionId,agentId)=>owners.filter(x=>agentId===undefined||agentId===x);
  const ref={hash:'fixture',size:1};
  const store={dataDir:'fixture-only',getSession:id=>({id,projectId:'project'}),listExecutionRuns:async()=>['parent-run','child-run','sibling-run'].map(id=>({id,turnId:id,code:ref,stdout:ref,stderr:ref})),getSessionPermissionEpoch:()=>null,listArtifacts:()=>[],listEnvironments:()=>[],listEnvironmentRevisions:()=>[],listSubagents:()=>[{id:'child'},{id:'sibling'}],captureSubagentAuthorities:async(sessionId,subagentId)=>[{id:subagentId}],notifications:{snapshot},transfers:{snapshot},shellExecutions:{snapshot},listReviews:async()=>[],listArtifactReviews:async()=>[]};
  const scope={sessionId:'session',executionId:'child-run',subagentId:'child'};
  const out=await(stage==='before'?context.replay(store,'session','parent-run'):context.replay(store,scope))();
  assert.equal(out.executions.length,1);
  assert.equal(out.executions[0].id,stage==='before'?'parent-run':'child-run');
  assert.equal(out.children.length,stage==='before'?2:0);
  assert.deepEqual(out.notifications,stage==='before'?owners:['subagent:child']);
  cases.push({id:`child-authority-scope-${stage}`,outcome:stage==='before'?'defect-present':'specific-defect-absent',checks:{executionIds:Array.from(out.executions,x=>x.id),childCatalogCount:out.children.length,taskId:out.task?.id??null,notificationOwners:out.notifications}});
}
const result={runtime:process.version,method:'Exact pinned TypeScript function sources stripped/transformed with built-in node:module; imports removed for isolated execution. Artifact helper and binary classifier are exact pinned sources. Authority snapshot dependencies use explicit in-memory stubs; invocation matches the verified before/fixed production binding.',limits:['No upstream test suite ran.','No actual SessionStore, SQLite, CAS, Runner, JiuwenSwarm or model was exercised.','Artifact replay checks terminal and beyond-window pages, not full agent pagination journeys.','Authority replay checks collector logic and selected owner arguments, not production persistence or permission policy.'],cases};
console.log(JSON.stringify(result,null,2));
