from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import zipfile,yaml,collections,csv
figdir=Path(__file__).resolve().parent/'figures'
figdir.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12})
fig,ax=plt.subplots(figsize=(6.6,5.8));ax.set_xlim(0,1);ax.set_ylim(-.025,1);ax.axis('off')
blue='#244960';light='#eef3f6'
def box(x,y,w,h,label):
 ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.015',fc=light,ec=blue,lw=1.2));ax.text(x,y,label,ha='center',va='center',fontsize=12,color=blue)
def arrow(a,b,label=None):
 ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color=blue,lw=1.4))
 if label: ax.text((a[0]+b[0])/2,(a[1]+b[1])/2,label,fontsize=9,ha='left',va='bottom')
for y,txt in [(0.89,'Producer\nArtifact + discrete claims'),(.68,'Deterministic checks\nStructure + references'),(.47,'Independent verifier\nClaims + source evidence'),(.26,'Advance gate\nEvidence + authorization'),(.07,'Next role')]:box(.32,y,.53,.115,txt)
for a,b in [(.83,.74),(.62,.53),(.41,.32),(.20,.13)]:arrow((.32,a),(.32,b))
box(.83,.48,.24,.15,'Technical\nlead')
arrow((.59,.26),(.83,.38));ax.text(.86,.25,'Block /\nreassign',ha='center',fontsize=10)
arrow((.83,.57),(.83,.89));arrow((.83,.89),(.60,.89));ax.text(.85,.72,'Revise\nscope',fontsize=10)
for ext in ['png','svg']:fig.savefig(figdir/f'01-evidence-workflow.{ext}',dpi=230,bbox_inches='tight',facecolor='white')
plt.close(fig)
g=yaml.safe_load((Path(__file__).resolve().parents[2]/'contratos/gates.yaml').read_text())['gates'];counts=collections.Counter(v['verificacion'] for v in g.values())
labels=[('manual','Manual'),('presencia_archivo','File presence'),('presencia_campos','Field presence'),('comparacion_hash','Hash comparison'),('umbral_numerico','Numeric threshold'),('umbral_severidad','Severity threshold')]
fig,ax=plt.subplots(figsize=(6.6,4.25));vals=[counts[k] for k,_ in labels];bars=ax.barh([v for _,v in labels],vals,color=['#b57736']+['#244960']*5,height=.57);ax.invert_yaxis();ax.set_xlim(0,8);ax.set_xticks(range(0,9,2));ax.set_xlabel('Number of declared gates');ax.bar_label(bars,padding=5);ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0);ax.set_axisbelow(True);ax.grid(axis='x',alpha=.18)
for ext in ['png','svg']:fig.savefig(figdir/f'02-declared-gates.{ext}',dpi=230,bbox_inches='tight',facecolor='white')
plt.close(fig)
with (figdir/'declared-gates.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['verification_type','label','count']);w.writerows((k,l,counts[k]) for k,l in labels)
