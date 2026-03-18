import itertools
import threading
import queue
import time
import random
import os
import re as _re
import string
import json
from colorama import init
from threading import Lock
import requests
import urllib3

TT_CONFIG_FILE = 'tiktok.json'

def _load_tt_config():
    try:
        with open(TT_CONFIG_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_tt_config(data):
    try:
        existing = _load_tt_config()
        existing.update(data)
        with open(TT_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=2)
    except Exception:
        pass


try:
    import discord
    from discord import app_commands
    DISCORD_BOT_AVAILABLE = True
except ImportError:
    DISCORD_BOT_AVAILABLE = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─────────────────────────────────────────────────────────────────────────────
# GERADORES OG — TikTok: 2-24 chars [a-z0-9_.] sem . no inicio/fim
# ─────────────────────────────────────────────────────────────────────────────

def og_style():
    l = string.ascii_lowercase; d = string.digits
    t = random.randint(0, 9)
    if t == 0: return random.choice(d)+''.join(random.choices(l,k=4))
    if t == 1: return ''.join(random.choices(l,k=2))+''.join(random.choices(d,k=2))+random.choice(l)
    if t == 2: return ''.join(random.choices(l,k=2))+'_'+random.choice(d)+random.choice(l)
    if t == 3: return ''.join(random.choices(l,k=2))+'_'+''.join(random.choices(l,k=2))
    if t == 4: return random.choice(l)+'_'+''.join(random.choices(d,k=2))+random.choice(l)
    if t == 5: return random.choice(d)+''.join(random.choices(l,k=3))
    if t == 6: return ''.join(random.choices(l,k=2))+'_'+random.choice(l)
    if t == 7: return random.choice(l)+'_'+random.choice(d)+random.choice(l)
    if t == 8: return ''.join(random.choices(l,k=2))+''.join(random.choices(d,k=2))
    return random.choice(d)+random.choice(l)+'_'+random.choice(l)+random.choice(d)

def og_repeat(min_len=5, max_len=5):
    l = string.ascii_lowercase; d = string.digits
    length = random.randint(min_len, max_len)
    if length == 2:
        t = random.randint(0, 1)
        if t == 0: c=random.choice(l); return c+c
        return random.choice(l)+random.choice(d)
    if length == 3:
        t = random.randint(0, 3)
        if t == 0: c=random.choice(l); return c+c+random.choice(d)
        if t == 1: c=random.choice(d); return c+c+random.choice(l)
        if t == 2: c=random.choice(l); return c+random.choice(d)+c
        return random.choice(d)+random.choice(l)+random.choice(d)
    if length == 4:
        t = random.randint(0, 5)
        if t == 0: cl=random.choice(l);cd=random.choice(d); return cl+cl+cd+cd
        if t == 1: c=random.choice(l); return c+c+random.choice(l)+random.choice(d)
        if t == 2: c=random.choice(d); return random.choice(l)+random.choice(l)+c+c
        if t == 3: c=random.choice(d); return c+c+random.choice(l)+random.choice(l)
        if t == 4: c=random.choice(l); return c+'_'+c+random.choice(d)
        c=random.choice(d); return random.choice(l)+random.choice(l)+'_'+c
    if length == 5:
        t = random.randint(0, 9)
        if t == 0: c=random.choice(d); return random.choice(l)+random.choice(l)+c+c+random.choice(l)
        if t == 1: c1=random.choice(l);c2=random.choice(d); return c1+c1+random.choice(l)+c2+c2
        if t == 2: c=random.choice(l); return random.choice(l)+random.choice(d)+c+c+random.choice(l)
        if t == 3: c=random.choice(l); return random.choice(l)+random.choice(l)+c+c+random.choice(d)
        if t == 4: a=random.choice(l);b=random.choice(d); return a+b+a+b+random.choice(l)
        if t == 5: c=random.choice(l); return c+c+'_'+random.choice(d)+random.choice(l)
        if t == 6: c=random.choice(d); return random.choice(l)+random.choice(l)+'_'+c+c
        if t == 7: c=random.choice(l); return random.choice(l)+random.choice(d)+c+c+random.choice(l)
        if t == 8: c=random.choice(d); return c+c+random.choice(l)+random.choice(l)+random.choice(l)
        c=random.choice(l); return random.choice(l)+'_'+c+c+random.choice(d)
    if length == 6:
        t = random.randint(0, 5)
        if t == 0: c=random.choice(d); return random.choice(l)+random.choice(l)+c+c+random.choice(l)+random.choice(l)
        if t == 1: c=random.choice(l); return c+c+random.choice(l)+random.choice(d)+random.choice(l)+random.choice(d)
        if t == 2: c=random.choice(l); return random.choice(l)+c+c+random.choice(d)+random.choice(d)+random.choice(l)
        if t == 3: c1=random.choice(l);c2=random.choice(d); return c1+c1+random.choice(l)+c1+c2+random.choice(l)
        if t == 4: c=random.choice(d); return random.choice(l)+random.choice(l)+'_'+c+c+random.choice(l)
        c=random.choice(l); return c+c+'_'+random.choice(l)+random.choice(d)+random.choice(d)
    if length == 7:
        t = random.randint(0, 3)
        if t == 0: c=random.choice(d); return random.choice(l)+random.choice(l)+c+c+random.choice(l)+random.choice(l)+random.choice(d)
        if t == 1: c=random.choice(l); return c+c+random.choice(d)+random.choice(d)+random.choice(l)+random.choice(l)+random.choice(d)
        if t == 2: a=random.choice(l);b=random.choice(d); return a+b+a+b+random.choice(l)+random.choice(l)+random.choice(d)
        c=random.choice(l); return random.choice(l)+random.choice(l)+'_'+c+c+random.choice(d)+random.choice(d)
    base = og_repeat(5, 5)
    chars = string.ascii_lowercase + string.digits
    suffix = ''.join(random.choice(chars) for _ in range(length - 5))
    return base + suffix

def target_tt(length):
    chars = string.ascii_lowercase + string.digits + '_'
    while True:
        u = ''.join(random.choice(chars) for _ in range(length))
        if not u.startswith('.') and not u.endswith('.') and '..' not in u:
            return u

def semi_tt():
    l = string.ascii_lowercase; d = string.digits
    return random.choice(l)+random.choice(l)+'_'+random.choice(l)+random.choice(d)

def letters_only_tt(mn=5, mx=6):
    """So letras, sem numeros, sem underscore. Ex: bryyk seeys oyyop nunch"""
    l = string.ascii_lowercase
    V = list('aeiou')
    C = list('bcdfghjklmnprstvwxyz')
    length = random.randint(mn, mx)
    for _ in range(200):
        t = random.randint(0, 10)
        if t == 0:
            c = random.choice(l); u = c+c+''.join(random.choices(l, k=length-2))
        elif t == 1:
            c1 = random.choice(l); c2 = random.choice(l)
            u = c1+c1+c2+c2+''.join(random.choices(l, k=max(0, length-4)))
        elif t == 2:
            half = ''.join(random.choices(l, k=length//2))
            u = half + (random.choice(l) if length % 2 else '') + half[::-1]
        elif t == 3:
            u = ''.join(random.choices(C, k=length))
        elif t == 4:
            v1 = random.choice(V); v2 = random.choice(V)
            u = v1 + ''.join(random.choices(l, k=length-2)) + v2
        elif t == 5:
            c = random.choice(l); u = c * length
        elif t == 6:
            parts = []
            while len(parts) < length:
                c = random.choice(l); parts.extend([c] * random.choice([1, 2]))
            u = ''.join(parts[:length])
        elif t == 7:
            c1 = random.choice(C); c2 = random.choice(C); v = random.choice(V)
            u = c1+c2+v+''.join(random.choices(l, k=max(0, length-3)))
        elif t == 8:
            v1 = random.choice(V); v2 = random.choice(V)
            u = v1+v2+''.join(random.choices(l, k=max(0, length-2)))
        elif t == 9:
            pre = random.choice(l); v = random.choice(V)
            u = pre+v+v+''.join(random.choices(l, k=max(0, length-3)))
        else:
            u = ''.join(random.choices(l, k=length))
        u = u[:length]
        if len(u) == length and u.isalpha() and is_valid_tt_username(u):
            return u
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def mixed_tt(mn=5, mx=6):
    """Letras + numeros, sem underscore. Ex: br66k n4n4v nr4h mx99k x65kk"""
    l = string.ascii_lowercase; d = string.digits
    length = random.randint(mn, mx)
    for _ in range(200):
        t = random.randint(0, 8)
        if t == 0:
            pre = ''.join(random.choices(l, k=random.randint(1, 2)))
            num = random.choice(d)
            post = ''.join(random.choices(l, k=max(0, length-len(pre)-2)))
            u = pre+num+num+post
        elif t == 1:
            parts = []; toggle = False
            for _ in range(length):
                parts.append(random.choice(d if toggle else l))
                if random.random() < 0.4: toggle = not toggle
            u = ''.join(parts)
        elif t == 2:
            u = ''.join(random.choices(l, k=length-1)) + random.choice(d)
        elif t == 3:
            u = random.choice(d) + ''.join(random.choices(l, k=length-1))
        elif t == 4:
            pos = random.randint(1, max(1, length-3))
            u = (''.join(random.choices(l, k=pos)) + random.choice(d) + random.choice(d)
                 + ''.join(random.choices(l, k=max(0, length-pos-2))))
        elif t == 5:
            chars = list(''.join(random.choices(l, k=length-1)))
            chars.insert(random.randint(1, length-1), random.choice(d))
            u = ''.join(chars[:length])
        elif t == 6:
            u = ''; toggle = False
            while len(u) < length:
                u += random.choice(d if toggle else l); toggle = not toggle
        elif t == 7:
            c = random.choice(l); n = random.choice(d)
            u = c+c+n+n+''.join(random.choices(l, k=max(0, length-4)))
        else:
            half1 = ''.join(random.choices(l, k=length//2-1))
            half2 = ''.join(random.choices(l, k=length-len(half1)-1))
            u = half1+random.choice(d)+half2
        u = u[:length]
        if (len(u) == length and is_valid_tt_username(u)
                and any(c.isdigit() for c in u) and '_' not in u):
            return u
    return ''.join(random.choices(l, k=length-1)) + random.choice(d)


def combined_tt(mn=5, mx=6):
    """3 so letras + 2 com numeros a cada 5 usernames."""
    combined_tt._counter = getattr(combined_tt, '_counter', 0) + 1
    if combined_tt._counter % 5 in (3, 4):
        return mixed_tt(mn, mx)
    return letters_only_tt(mn, mx)


def rare_tt(mn=4, mx=5):
    """
    Gera usernames raros/caros estilo TikTok OG.
    
    O que define um username raro no TikTok:
      - 4-5 chars (4 = mais valioso, ~456k combinações totais)
      - Sem underscore, sem ponto
      - Pronunciável ou parecido com palavra real
      - No máximo 1-2 substituições leet: ea6ts h0tel n1ght bl4de
      - Consonant clusters com número: br66k sp5td nrk7t
      - Parece "limpo" e original
    
    Padrões gerados:
      VCNCC: ea6ts ou7rs  (vowel + cons + num + cons + cons)
      CVNCC: la3ts be4st  (cons + vowel + num + cons + cons)
      CCNCC: br66k sp5td  (cons + cons + num + cons + cons)
      VCCNC: outs6 elts3  (vowel + cons + cons + num + cons)
      Word+leet: h0tel n1ght bl4de gr4ce  (palavra real com leet)
      Pure consonants: spzpd nrtkv bryyk  (4-5 consoantes)
      CCVCC: brisk flame  (consonant-vowel sandwich)
    """
    l = string.ascii_lowercase
    V = list('aeiou')
    C = list('bcdfghjklmnprstvwxyz')
    D = list('0123456789')

    # leet map — letter to number
    LEET = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0',
        's': '5', 'g': '9', 't': '7', 'b': '6',
        'l': '1', 'z': '2',
    }

    # short real-word bases for leet substitution
    WORDS4 = ['beat','best','bite','bits','belt','bolt','boat','boot','bond',
              'bend','blog','bold','bond','born','both','buff','bulk','bull',
              'bite','byte','cage','call','calm','came','cant','cash','cast',
              'chat','chop','cite','clap','claw','clay','clip','club','code',
              'coil','cold','colt','come','cool','cope','core','corn','cost',
              'coup','crew','crop','ctrl','cube','cult','damp','dark','dash',
              'data','date','dawn','days','dead','deal','dean','debt','deck',
              'deep','deny','desk','dial','diet','dirt','disk','dive','dock',
              'dope','dose','duel','dull','dump','dusk','dust','duty','each',
              'earl','earn','ease','east','eats','edge','emit','epic','even',
              'evil','exam','exit','expo','fact','fade','fail','fair','fake',
              'fall','fame','farm','fast','fate','fear','feat','feed','feel',
              'felt','file','fill','film','find','fine','fire','firm','fist',
              'five','flag','flat','flex','flip','flow','foam','foil','fold',
              'font','ford','fore','fork','form','fort','free','from','fuel',
              'full','fuse','gain','gale','game','gang','gate','gave','gaze',
              'gear','germ','gift','give','glad','glow','glue','gold','golf',
              'gone','good','gore','gory','grab','grim','grip','grit','grow',
              'gulf','gust','hack','hail','half','hall','halt','hand','hang',
              'hard','harm','harp','hash','hate','haze','head','heal','heat',
              'heel','held','helm','help','here','hero','hide','high','hill',
              'hint','hire','hits','hold','hole','home','hook','hope','horn',
              'host','hour','huge','hull','hunt','hurt','hypo','iced','icon',
              'idle','inks','into','ions','iris','iron','isle','itch','item',
              'jolt','jump','just','keen','kept','kick','kind','king','knot',
              'know','lack','laid','land','lane','laps','lash','last','late',
              'lava','lead','leak','lean','leap','left','less','lick','life',
              'lift','like','lime','line','link','list','live','load','lock',
              'loft','lone','long','lore','lose','loss','lost','lots','loud',
              'love','luck','lung','lure','made','main','make','mall','many',
              'mark','mars','mash','mass','mast','mate','math','maze','meal',
              'mean','meet','melt','mesh','mild','milk','mill','mind','mine',
              'mint','miss','mist','mode','moon','more','most','move','much',
              'muse','must','myth','nail','name','nerd','nest','next','nine',
              'node','nook','norm','note','null','numb','oath','obey','only',
              'open','orca','ores','owed','owns','pace','pack','pact','pain',
              'pale','palm','past','path','peak','peel','peer','pick','pier',
              'pile','pill','pine','ping','pipe','pits','plan','play','plot',
              'plus','poke','pole','poll','pond','pool','port','pose','post',
              'pour','pray','prey','prod','puff','pull','pure','push','quit',
              'race','raid','rail','rain','rank','rare','rats','rays','real',
              'reel','rely','rent','rest','rice','rich','ride','ring','riot',
              'rips','rise','risk','road','roam','roar','robe','rock','role',
              'roll','roof','ruin','rule','runs','rush','rust','safe','sage',
              'sail','sake','sale','salt','same','sand','seal','seam','seat',
              'seed','seek','self','sell','send','sent','shed','ship','shop',
              'shot','show','shut','sign','silk','silo','sine','sink','site',
              'size','skin','skip','slam','slap','slim','slip','slot','slow',
              'slug','snap','snow','soft','soil','sole','some','song','soon',
              'soul','sort','span','spit','spot','spur','star','stay','step',
              'stem','stir','stop','stub','such','suit','swap','swim','sync',
              'tabs','tack','tail','tale','talk','tall','tank','task','tear',
              'tell','tend','term','test','then','they','this','tide','tied',
              'tier','till','time','tiny','tips','tire','told','toll','tome',
              'took','tool','tops','tore','torn','toss','tour','town','toys',
              'tray','tree','trim','trip','true','tuck','tune','turf','turn',
              'twin','type','unit','upon','used','user','vane','vary','vast',
              'vein','very','vest','view','vine','void','volt','vows','wade',
              'wait','wake','walk','wall','warp','wars','wash','wave','ways',
              'weak','weld','well','went','west','what','when','whip','whom',
              'wide','wild','will','wilt','wins','wire','wish','with','woke',
              'wolf','wood','word','wore','work','worm','worn','wove','wrap',
              'writ','yard','year','yell','your','zero','zone','zoom']

    WORDS5 = ['beast','blade','bland','blank','blast','blaze','blend','block',
              'blood','bloom','blown','blues','blunt','board','boost','bound',
              'brace','brand','brave','brawn','bream','breed','brick','bride',
              'brief','brine','brink','brisk','broke','brood','brook','brown',
              'brush','built','burst','buyer','cable','carry','cause','cease',
              'chain','chair','chalk','chaos','charm','chase','check','chess',
              'chest','chief','child','chord','churn','claim','clamp','clank',
              'clash','class','clean','clear','clerk','click','cling','close',
              'cloud','coast','comet','could','count','court','cover','craft',
              'crane','crank','crash','crave','crawl','craze','creak','creek',
              'creep','crisp','cross','crowd','crown','crush','curve','cycle',
              'daily','dance','death','decay','dense','depth','devil','digit',
              'ditch','dodge','doing','doubt','dough','draft','drain','drawl',
              'drawn','dream','dress','drift','drill','drink','drive','drone',
              'drove','droop','drops','drove','drown','dryer','dwarf','dwell',
              'eagle','early','earth','eight','elite','empty','enemy','enjoy',
              'enter','equal','error','ether','event','every','exact','exist',
              'extra','fable','faith','falls','false','fault','feast','fence',
              'field','fifth','fifty','fight','final','first','fixed','flame',
              'flare','flash','flask','fleet','flesh','flies','float','flood',
              'floor','focus','force','forge','forth','forum','found','frame',
              'frank','fraud','fresh','front','frost','froze','fully','gains',
              'gamma','gavel','ghost','given','glare','glass','gleam','glide',
              'glint','gloat','gloom','gloss','glove','grace','grade','grain',
              'grand','grant','grasp','grass','grave','graze','greed','greet',
              'grief','grind','groan','grope','gross','group','grout','gruel',
              'guard','guess','guest','guide','guile','guild','guise','gusto',
              'gypsy','halve','hands','handy','happy','harsh','haste','haven',
              'heads','heart','heavy','hence','hinge','hippo','horde','hotel',
              'house','human','humid','hurry','hyper','ideal','image','imply',
              'infer','inner','input','inter','intro','issue','ivory','jaunt',
              'judge','juicy','keeps','kneel','knife','knock','known','label',
              'large','laser','latch','later','laugh','layer','leads','learn',
              'least','ledge','legal','level','light','limit','linen','liver',
              'liver','local','lodge','logic','loose','lower','lucky','magic',
              'major','maker','manor','march','match','mayor','media','mercy',
              'merge','metal','might','mixed','model','money','month','moral',
              'motor','mount','mouse','mouth','moved','movie','muddy','multi',
              'music','named','nasty','never','night','noise','north','noted',
              'novel','nurse','nymph','often','older','onset','order','other',
              'outer','owner','oxide','ozone','paint','panel','panic','paper',
              'party','patch','pause','payee','peace','penny','perch','phase',
              'phone','photo','pilot','pinch','pitch','pixel','place','plain',
              'plait','plane','plant','plate','plaza','pluck','plume','plunk',
              'plush','point','polar','poppy','power','press','price','pride',
              'prime','print','prior','prize','probe','proof','prose','prove',
              'prowl','psalm','pulse','punch','pupil','queen','query','quest',
              'queue','quick','quiet','quite','quota','quote','range','rapid',
              'ratio','reach','react','realm','rebel','reign','repay','reply',
              'repro','reset','resin','reuse','revue','ridge','rifle','right',
              'rivet','robin','robot','rouge','rough','round','route','rover',
              'royal','rugby','rumor','rural','safer','saint','sauce','scale',
              'scare','scene','scope','score','scout','screw','seize','sense',
              'serve','seven','shade','shaft','shake','shale','shame','shape',
              'share','sharp','shelf','shell','shift','shine','shire','shirt',
              'shore','short','sigma','sixth','sixty','sized','skill','slash',
              'slate','sleep','sleek','slick','slide','slope','slump','slunk',
              'smack','small','smart','smash','smell','smile','smite','smoke',
              'solar','solid','solve','sound','south','space','spare','spark',
              'spawn','speed','spell','spend','spice','spike','spine','spite',
              'split','spoke','spook','spray','spree','squad','squat','stab',
              'stack','staff','stage','stain','stake','stale','stall','stamp',
              'stand','stank','stark','start','state','steal','steam','steel',
              'steer','stern','stick','stiff','still','sting','stomp','stone',
              'store','storm','story','stout','strut','stuck','study','stump',
              'stunt','style','sugar','suite','sully','sumac','super','surge',
              'swamp','swarm','swath','swear','sweep','sweet','swept','swift',
              'swipe','swirl','sword','swore','sworn','swung','syrup','table',
              'taunt','teach','tense','terms','their','theme','there','thick',
              'thing','third','those','three','throw','thumb','tiger','tight',
              'timer','tinge','tints','tired','title','toast','today','token',
              'total','touch','tough','towel','toxic','trace','track','trade',
              'trail','train','trait','tramp','trash','trial','tribe','trick',
              'tried','troll','troop','troth','trout','trove','truce','truck',
              'truly','trump','trunk','truss','trust','truth','tulip','tumor',
              'tuner','turbo','tutor','twirl','twist','ultra','under','union',
              'until','upper','urban','usher','usual','utter','vague','valid',
              'value','valve','vapor','verse','vinyl','viral','virus','visor',
              'visit','vital','vivid','vocal','vodka','vomit','voter','vowed',
              'vulva','waste','watch','water','weave','weedy','weigh','weird',
              'weary','wheel','where','which','while','white','whole','whose',
              'wider','woman','women','world','worse','worst','worth','would',
              'wound','wrath','wreck','wring','wrist','wrote','yacht','young',
              'youth','zebra','zilch']

    length = random.randint(mn, mx)

    for _ in range(300):
        t = random.randint(0, 11)

        # ── Patterns that generate OG/rare style usernames ───────────────────

        if t == 0:
            # VCNCC — ea6ts ou7rs: vowel + cons + digit + cons + cons (5 chars)
            # Only for length 5
            if length == 5:
                v  = random.choice(V)
                c1 = random.choice(C)
                n  = random.choice(D)
                c2 = random.choice(C)
                c3 = random.choice(C)
                u  = v+c1+n+c2+c3
            else:
                u = random.choice(V)+random.choice(C)+random.choice(D)+random.choice(C)

        elif t == 1:
            # CVNCC — be4st la3ts: cons + vowel + digit + cons + cons
            c1 = random.choice(C)
            v  = random.choice(V)
            n  = random.choice(D)
            c2 = random.choice(C)
            rest = ''.join(random.choices(C, k=max(0, length-4)))
            u = (c1+v+n+c2+rest)[:length]

        elif t == 2:
            # CCNCC — br66k sp5td: cons + cons + digit + cons + cons
            c1 = random.choice(C)
            c2 = random.choice(C)
            n  = random.choice(D)
            c3 = random.choice(C)
            rest = ''.join(random.choices(C, k=max(0, length-4)))
            u = (c1+c2+n+c3+rest)[:length]

        elif t == 3:
            # Pure consonants — spzpd nrtkv bryyk (no vowels, no numbers)
            # These ARE rare: look clean and random
            u = ''.join(random.choices(C, k=length))

        elif t == 4:
            # Word + 1 leet substitution — h0tel n1ght bl4de
            words = WORDS4 if length == 4 else WORDS5
            base = random.choice(words)
            # find substitutable positions
            subs = [i for i, c in enumerate(base) if c in LEET]
            if not subs:
                continue
            pos = random.choice(subs)
            u = base[:pos] + LEET[base[pos]] + base[pos+1:]

        elif t == 5:
            # CCVCC — brisk flame: consonant sandwich (rare, pronounceable)
            c1 = random.choice(C)
            c2 = random.choice(C)
            v  = random.choice(V)
            c3 = random.choice(C)
            rest = ''.join(random.choices(C, k=max(0, length-4)))
            u = (c1+c2+v+c3+rest)[:length]

        elif t == 6:
            # VCCNC — outs6 ilts3: vowel cluster + number at end
            v  = random.choice(V)
            c1 = random.choice(C)
            c2 = random.choice(C)
            n  = random.choice(D)
            rest = ''.join(random.choices(C, k=max(0, length-4)))
            u = (v+c1+c2+n+rest)[:length]

        elif t == 7:
            # NCC+CC — 6r4ts 0f7sp: starts with number
            n1 = random.choice(D)
            c1 = random.choice(C)
            n2 = random.choice(D)
            rest = ''.join(random.choices(C, k=max(0, length-3)))
            u = (n1+c1+n2+rest)[:length]
            # must not start with number for TikTok validity check
            # skip this since TikTok allows numbers anywhere

        elif t == 8:
            # Word leet — 4 chars: b3st d4rk n1ght (short)
            words = WORDS4 if length <= 4 else WORDS5
            base = random.choice(words)[:length]
            if len(base) != length:
                continue
            subs = [i for i, c in enumerate(base) if c in LEET]
            if len(subs) >= 1:
                # pick 1-2 positions max for clean look
                n_subs = min(2, len(subs))
                for pos in random.sample(subs, n_subs):
                    base = base[:pos] + LEET[base[pos]] + base[pos+1:]
            u = base

        elif t == 9:
            # CVCNN — bla66 spe99: word start + double number end
            c1 = random.choice(C)
            v  = random.choice(V)
            c2 = random.choice(C)
            n  = random.choice(D)
            rest = ''.join([n]*max(0, length-4) if random.random()<0.5
                           else random.choices(D, k=max(0, length-4)))
            u = (c1+v+c2+n+rest)[:length]

        elif t == 10:
            # Double number embedded — br66k n44v: consonants with repeated digit
            c1 = random.choice(C)
            c2 = random.choice(C)
            n  = random.choice(D)
            c3 = random.choice(C)
            rest = ''.join(random.choices(C, k=max(0, length-4)))
            u = (c1+c2+n+n+c3+rest)[:length]  # double same digit

        else:
            # CVC leet — mix of pronounceable + leet
            cv = random.choice([c+v for c in C for v in V])
            c_end = ''.join(random.choices(C, k=max(0, length-3)))
            n_pos = random.randint(0, len(cv)-1)
            base = cv + c_end
            base = base[:length]
            subs = [i for i, c in enumerate(base) if c in LEET]
            if subs:
                pos = random.choice(subs)
                base = base[:pos]+LEET[base[pos]]+base[pos+1:]
            u = base

        u = u[:length].lower()

        # Validate: correct length, only [a-z0-9], no leading digit for TikTok
        if (len(u) == length
                and _re.match(r'^[a-z0-9]+$', u)
                and not u.isdigit()
                and len(set(u.replace('0','o').replace('1','i')
                              .replace('3','e').replace('4','a')
                              .replace('5','s').replace('6','b')
                              .replace('7','t').replace('9','g'))) >= 3):
            return u

    # fallback — 4-5 consonants
    return ''.join(random.choices(C, k=length))


def _fetch_word_api(length, lang='en'):
    """
    Fetches a random word from random-word-api.herokuapp.com.
    Supports: en, es, de, fr, it, pt, nl, fi, sv, pl, cs, sk, hu, ro, tr
    No API key needed. Returns word string or None on failure.
    """
    try:
        r = requests.get(
            'https://random-word-api.herokuapp.com/word',
            params={'number': 5, 'lang': lang, 'length': length},
            timeout=4
        )
        if r.status_code == 200:
            words = r.json()
            if words and isinstance(words, list):
                # filter: only ascii letters, exact length
                valid = [w.lower() for w in words
                         if w.isascii() and w.isalpha() and len(w) == length]
                if valid:
                    return random.choice(valid)
    except Exception:
        pass
    return None


# Cache for API words to avoid too many requests
_word_cache = []
_word_cache_lock = None

def _get_cached_word(length):
    """Get a word from cache or fetch batch from API."""
    global _word_cache, _word_cache_lock
    import threading as _th
    if _word_cache_lock is None:
        _word_cache_lock = _th.Lock()

    LANGS = ['en', 'es', 'de', 'fr', 'it', 'pt', 'nl', 'pl', 'sv', 'fi', 'cs', 'tr']
    with _word_cache_lock:
        # filter cache for matching length
        matching = [w for w in _word_cache if len(w) == length]
        if matching:
            word = random.choice(matching)
            _word_cache = [w for w in _word_cache if w != word]
            return word

    # cache empty — fetch batch
    lang = random.choice(LANGS)
    word = _fetch_word_api(length, lang)
    if word:
        return word
    # also try without length constraint
    try:
        r = requests.get(
            'https://random-word-api.herokuapp.com/word',
            params={'number': 20, 'lang': lang},
            timeout=4
        )
        if r.status_code == 200:
            words = r.json()
            valid = [w.lower() for w in words
                     if w.isascii() and w.isalpha()
                     and 4 <= len(w) <= 8]
            with _word_cache_lock:
                _word_cache.extend(valid)
            matching = [w for w in valid if len(w) == length]
            if matching:
                return random.choice(matching)
    except Exception:
        pass
    return None


def multilang_tt(mn=4, mx=6):
    """
    Gera usernames baseados em palavras de dicionarios de varios idiomas.
    Usa a API random-word-api.herokuapp.com (gratuita, sem chave).
    Idiomas: EN, ES, DE, FR, IT, PT, NL, PL, SV, FI, CS, TR.
    Fallback: lista offline se API indisponivel.
    """
    LEET = {'a':'4','e':'3','i':'1','o':'0','s':'5','g':'9','t':'7','b':'6','l':'1'}
    length = random.randint(mn, mx)

    for _ in range(30):
        # try API first
        base = _get_cached_word(length)

        # fallback to offline list
        if not base:
            OFFLINE = [
                'amor','azul','belo','sol','mar','vento','forte','noite',
                'best','blade','storm','frost','night','dream','swift',
                'amor','cielo','dulce','largo','noche','nuevo','frio',
                'ciel','joie','fort','nuit','beau','vrai','sage',
                'stark','nacht','welt','licht','kraft','leben','traum',
                'cuore','notte','forte','vento','mare','bello','luce',
                'yuki','hana','kaze','yoru','hoshi','tsuki','hikari',
                'kalt','warm','grau','blau','rosa','grun','gold',
            ]
            base = random.choice([w for w in OFFLINE if abs(len(w)-length)<=1])
            base = base[:length].ljust(length, random.choice('aeiou'))

        base = base.lower()[:length]
        if len(base) < 3:
            continue

        t = random.randint(0, 4)
        if t == 0:
            u = base  # pure word
        elif t == 1:
            # 1 leet substitution
            subs = [i for i, c in enumerate(base) if c in LEET]
            if subs:
                p = random.choice(subs)
                u = base[:p] + LEET[base[p]] + base[p+1:]
            else:
                u = base
        elif t == 2:
            u = base[:-1] + random.choice('0123456789')
        elif t == 3:
            u = random.choice('0123456789') + base[1:]
        else:
            u = base[::-1]  # reversed

        u = u[:length].lower()
        if (len(u) == length
                and _re.match(r'^[a-zA-Z0-9_.]{4,24}$', u)
                and not u.isdigit()
                and is_valid_tt_username(u)):
            return u

    return base[:length] if base else ''.join(random.choices('abcdefghijklmnoprstuvwxyz', k=length))


_TT_VALID = _re.compile(r'^[a-zA-Z0-9_.]{4,24}$')

def is_valid_tt_username(u: str) -> bool:
    if not _TT_VALID.match(u): return False
    if u.startswith('.') or u.endswith('.'): return False
    if '..' in u: return False
    if u.isdigit(): return False
    # TikTok reserves names with fewer than 4 distinct chars
    # Examples blocked: xxxxx hhhhh rrxxc bbuuw ffppoo n44n4
    alnum = [c for c in u if c.isalnum()]
    if len(set(alnum)) < 4: return False
    return True

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACOES
# ─────────────────────────────────────────────────────────────────────────────

SETTINGS_FILE   = 'DCsettings.txt'
BOT_CONFIG_FILE = 'tt_bot_config.json'
BOT_HITS_FILE   = 'hitsusernames.txt'

def _load_settings():
    try:
        with open(SETTINGS_FILE) as f:
            s = f.read()
        webhook = s.split('Webhook:[')[1].split(']')[0].strip()
        token = ''
        try: token = s.split('Token:[')[1].split(']')[0].strip()
        except IndexError: pass
        return webhook, token
    except (FileNotFoundError, IndexError):
        print("\n" + "="*52)
        print("  CONFIGURACAO — TikTok Sniper")
        print("  (usa o mesmo DCsettings.txt do Discord Sniper)")
        print("="*52)
        webhook = input("  Discord Webhook: ").strip()
        token   = input("  Bot Token (Enter para pular): ").strip()
        with open(SETTINGS_FILE, 'w') as f:
            f.write(f"Webhook:[{webhook}]\nToken:[{token}]\n")
        print(f"\n  Salvo em {SETTINGS_FILE}\n")
        return webhook, token

def _bot_load_config():
    try:
        with open(BOT_CONFIG_FILE) as f: return json.load(f)
    except Exception: return {'only_available': True}

def _bot_save_config(cfg):
    try:
        with open(BOT_CONFIG_FILE, 'w') as f: json.dump(cfg, f)
    except Exception: pass

def _bot_count_hits():
    try:
        with open(BOT_HITS_FILE, encoding='utf-8') as f:
            return [l.strip() for l in f if l.strip()]
    except FileNotFoundError: return []

# ─────────────────────────────────────────────────────────────────────────────
# BOT DISCORD
# ─────────────────────────────────────────────────────────────────────────────

def start_discord_bot(token):
    if not token or not DISCORD_BOT_AVAILABLE: return
    intents = discord.Intents.default()
    client  = discord.Client(intents=intents)
    tree    = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        await tree.sync()
        print(f'  [BOT] Online: {client.user}')

    @tree.command(name='tt_check_available', description='TikTok: controla o que o sniper envia')
    @app_commands.describe(modo='on = somente disponiveis | off = tudo')
    @app_commands.choices(modo=[
        app_commands.Choice(name='on  — somente disponiveis', value='on'),
        app_commands.Choice(name='off — disponiveis + indisponiveis', value='off'),
    ])
    async def check_available(interaction: discord.Interaction, modo: str):
        cfg = _bot_load_config(); cfg['only_available'] = (modo == 'on')
        _bot_save_config(cfg)
        cor = 0x00ff00 if modo == 'on' else 0x5865f2
        titulo = 'TikTok: somente disponiveis' if modo == 'on' else 'TikTok: tudo'
        await interaction.response.send_message(embed=discord.Embed(title=titulo, color=cor))

    @tree.command(name='tt_info', description='TikTok: estatisticas')
    async def info(interaction: discord.Interaction):
        hits = _bot_count_hits(); cfg = _bot_load_config()
        modo = 'somente disponiveis' if cfg.get('only_available', True) else 'tudo'
        embed = discord.Embed(title='TikTok Sniper Stats', color=0x5865f2)
        embed.add_field(name='Disponiveis', value=str(len(hits)), inline=True)
        embed.add_field(name='Modo',        value=modo,           inline=True)
        await interaction.response.send_message(embed=embed)

    threading.Thread(target=lambda: client.run(token, log_handler=None), daemon=True).start()

# ─────────────────────────────────────────────────────────────────────────────
# CHECKER
# ─────────────────────────────────────────────────────────────────────────────

class TikTokChecker:

    @staticmethod
    def _log(tag, msg):
        line = f"[{time.strftime('%H:%M:%S')}] [{tag}] {msg}"
        # imprime apenas eventos criticos no terminal
        if tag in ('RL', 'PROXY', 'THREADS'):
            print(f'\r\033[K\033[33m  [{tag}] {msg}\033[0m')
        try:
            with open('smth.log', 'a', encoding='utf-8') as f: f.write(line + '\n')
        except Exception: pass

    TT_MIN_LEN = 4

    # ── Sigil adapts to terminal width automatically ────────────────────────
    @classmethod
    def get_sigil(cls):
        """Display msk.jpg with chafa if available, else show nothing."""
        import subprocess, shutil as _sh
        if _sh.which('chafa'):
            cols = _sh.get_terminal_size(fallback=(60, 24)).columns
            size = f"{min(cols, 55)}x28"
            try:
                subprocess.run(['chafa', '--size', size, 'msk.jpg'],
                               check=False)
                return ''
            except Exception:
                pass
        return ''



    LANG = {
        'pt': {
            'save':     'Salvar hits em hitsusernames.txt? (S/N) [S]: ',
            'webhook':  'Discord Webhook (Enter para pular): ',
            'mode': (
                "Modo de geracao [1/2/3/4/5]\n"
                "  1 - So letras    (bryyk seeys oyyop nunch)\n"
                "  2 - Com numeros  (br66k n4n4v nr4h mx99k)\n"
                "  3 - Combinado 3:2 (3 letras + 2 com numero)\n"
                "  4 - Raro/Caro    (ea6ts h0tel n1ght) <- RECOMENDADO\n"
                "  5 - Dicionario   (amor sol yuki baka)\n"
                "Opcao: "
            ),
            'range':    'Range de tamanho (ex: 5-7  4-5  5-6): ',
            'range_err':'  Invalido. Min 4. Ex: 5-7',
            'threads':  'Numero de threads [1]: ',
            'avail':    '\033[32m{} disponivel no tiktok #ea6ts ig\033[0m',
            'taken':    '\033[31m{} indisponivel no tiktok #ea6ts ig\033[0m',
            'checking': '\033[90mchecando @{}\033[0m',
            'rl':       '\033[33mrate limit {}s...\033[0m',
            'threads_started': '{} threads iniciadas',
            'wh_msg':   '`{}` available on tiktok #ea6ts ig',
        },
        'en': {
            'save':     'Save hits to hitsusernames.txt? (Y/N) [Y]: ',
            'webhook':  'Discord Webhook (Enter to skip): ',
            'mode': (
                "Generation mode [1/2/3/4/5]\n"
                "  1 - Letters only  (bryyk seeys oyyop nunch)\n"
                "  2 - With numbers  (br66k n4n4v nr4h mx99k)\n"
                "  3 - Combined 3:2  (3 letters + 2 with number)\n"
                "  4 - Rare/OG       (ea6ts h0tel n1ght) <- RECOMMENDED\n"
                "  5 - Dictionary    (amor sol yuki baka)\n"
                "Option: "
            ),
            'range':    'Length range (e.g. 5-7  4-5  5-6): ',
            'range_err':'  Invalid. Min 4. Ex: 5-7',
            'threads':  'Number of threads [1]: ',
            'avail':    '\033[32m{} available on tiktok #ea6ts ig\033[0m',
            'taken':    '\033[31m{} not available on tiktok #ea6ts ig\033[0m',
            'checking': '\033[90mchecking @{}\033[0m',
            'rl':       '\033[33mrate limit {}s...\033[0m',
            'threads_started': '{} threads started',
            'wh_msg':   '`{}` available on tiktok #ea6ts ig',
        },
    }

    def __init__(self):
        os.system("cls" if os.name == 'nt' else "clear")

        self.lock        = Lock()
        self.go          = True
        self.att         = 0
        self.Rl          = 0
        self.available   = 0
        self.thread_status = {}
        self.n_threads   = 1
        self.using_proxy = False
        self.checker_mod = '4'
        self.og_min      = 5
        self.og_max      = 6
        self._uidx       = 0
        self.length      = 5

        # ── idioma ────────────────────────────────────────────────────────
        TikTokChecker.get_sigil()
        print("  Idioma / Language:")
        print("  1 - Portugues BR")
        print("  2 - English")
        lang_raw = input("  Opcao: ").strip()
        self._L = TikTokChecker.LANG['en' if lang_raw == '2' else 'pt']
        os.system("cls" if os.name == 'nt' else "clear")

        # ── salvar hits ───────────────────────────────────────────────────
        TikTokChecker.get_sigil()
        save_raw = input("  " + self._L['save']).strip().upper()
        self.save_hits = (save_raw not in ('N','NO','NAO'))
        os.system("cls" if os.name == 'nt' else "clear")

        # ── webhook — carrega do tiktok.json ─────────────────────────────
        TikTokChecker.get_sigil()
        _saved_wh = _load_tt_config().get('webhook', '')
        if _saved_wh:
            print(f"  Webhook salvo: {_saved_wh[:40]}...")
            _keep = input("  Usar este? (S/N) [S]: ").strip().upper()
            if _keep == 'N':
                wh = input("  " + self._L['webhook']).strip()
                self.webhook = wh
                if wh: _save_tt_config({'webhook': wh})
            else:
                self.webhook = _saved_wh
        else:
            wh = input("  " + self._L['webhook']).strip()
            self.webhook = wh or ''
            if wh: _save_tt_config({'webhook': wh})
        os.system("cls" if os.name == 'nt' else "clear")

        if not os.path.exists(BOT_CONFIG_FILE): _bot_save_config({'only_available': True})

        # ── modo de geracao ───────────────────────────────────────────────
        TikTokChecker.get_sigil()
        self.checker_mod = input("  " + self._L['mode']).strip() or '4'
        # map 1-5 to internal: 1=letters_only, 2=mixed, 3=combined, 4=rare, 5=multilang
        _mode_map = {'1':'2','2':'3','3':'4','4':'5','5':'10'}
        self.checker_mod = _mode_map.get(self.checker_mod, '5')

        os.system("cls" if os.name == 'nt' else "clear")
        TikTokChecker.get_sigil()
        while True:
            raw = input("  " + self._L['range']).strip()
            if '-' in raw:
                try:
                    mn, mx = map(int, raw.split('-', 1))
                    if 4 <= mn <= mx <= 24:
                        self.og_min, self.og_max = mn, mx; break
                except Exception: pass
            print(self._L['range_err'])
        os.system("cls" if os.name == 'nt' else "clear")

        # ── threads ───────────────────────────────────────────────────────
        TikTokChecker.get_sigil()
        t_raw = input("  " + self._L['threads']).strip()
        self.n_threads = int(t_raw) if t_raw.isdigit() and int(t_raw) > 0 else 1
        os.system("cls" if os.name == 'nt' else "clear")

        # ── start ─────────────────────────────────────────────────────────
        threading.Thread(target=self._printer, daemon=True).start()

        if self.n_threads > 1:
            self._run_threaded()
        else:
            self._run_classic()

    # ── utils ─────────────────────────────────────────────────────────────────

    def _load_lines(self, path):
        try:
            with open(path) as f: return [l.strip() for l in f if l.strip()]
        except Exception as e:
            self._log('FILE', f'Erro: {e}'); return []

    def _load_proxies(self, path):
        lines = self._load_lines(path)
        self.proxy_list = [l for l in lines if ':' in l]
        self._log('PROXY', f'{len(self.proxy_list)} proxies de {path}')

    def _build_proxy(self, raw):
        if not raw: return None
        if self._ptype == '2': return {'http': f'socks4://{raw}', 'https': f'socks4://{raw}'}
        if self._ptype == '3': return {'http': f'socks5://{raw}', 'https': f'socks5://{raw}'}
        return {'http': f'http://{raw}', 'https': f'http://{raw}'}

    def _next_proxy_raw(self):
        with self._proxy_lock:
            if not self.proxy_list: return None
            now = time.time()
            for _ in range(len(self.proxy_list)):
                raw = next(self._proxy_cycle)
                if raw in self.proxy_dead: continue
                if self.proxy_rl.get(raw, 0) <= now: return raw
            vivas = [p for p in self.proxy_list if p not in self.proxy_dead]
            if not vivas: return None
            raw = min(vivas, key=lambda p: self.proxy_rl.get(p, 0))
            wait = self.proxy_rl.get(raw, 0) - now
            if wait > 0:
                self._log('PROXY', f'Todas em RL. Aguardando {wait:.0f}s por {raw}')
                time.sleep(wait + 0.3)
            return raw

    def _kill_proxy(self, raw):
        with self._proxy_lock:
            if not raw: return
            self.proxy_fails[raw] = self.proxy_fails.get(raw, 0) + 1
            if self.proxy_fails[raw] >= 3:
                self._log('PROXY', f'Proxy {raw} removida')
                self.proxy_dead.add(raw)
                self.proxy_fails.pop(raw, None)
                self.proxy_rl.pop(raw, None)

    def _mark_proxy_rl(self, raw, seconds):
        with self._proxy_lock:
            if raw: self.proxy_rl[raw] = time.time() + seconds

    def _gen_username(self):
        for _ in range(100):
            if self.checker_mod == '1':
                with self.lock:
                    if not self.usernames: return None
                    if self._uidx >= len(self.usernames): self._uidx = 0
                    u = self.usernames[self._uidx]; self._uidx += 1
            elif self.checker_mod == '2': u = letters_only_tt(self.og_min, self.og_max)
            elif self.checker_mod == '3': u = mixed_tt(self.og_min, self.og_max)
            elif self.checker_mod == '4': u = combined_tt(self.og_min, self.og_max)
            elif self.checker_mod == '5': u = rare_tt(self.og_min, self.og_max)
            elif self.checker_mod == '6': u = target_tt(self.length)
            elif self.checker_mod == '7': u = semi_tt()
            elif self.checker_mod == '8': u = og_style()
            elif self.checker_mod == '9': u = og_repeat(self.og_min, self.og_max)
            elif self.checker_mod == '10': u = multilang_tt(self.og_min, self.og_max)
            else: return None
            if len(u) >= self.TT_MIN_LEN and is_valid_tt_username(u):
                return u
        return None

    def _set_status(self, tid, username=None, status=None, rl=0):
        with self.lock:
            if tid not in self.thread_status:
                self.thread_status[tid] = {}
            if username is not None: self.thread_status[tid]['username'] = username
            if status   is not None: self.thread_status[tid]['status']   = status
            if rl > 0:               self.thread_status[tid]['rl'] = time.time() + rl
            elif rl == -1:           self.thread_status[tid]['rl'] = 0

    # ── UAs ───────────────────────────────────────────────────────────────────

    _UAS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    ]

    # ── check ─────────────────────────────────────────────────────────────────
    #
    # LOGICA CORRIGIDA — por que a versao anterior errava:
    #
    #   O TikTok oEmbed retorna:
    #     HTTP 200 + JSON  →  usuario EXISTE           → TOMADO
    #     HTTP 400         →  usuario NAO existe       → DISPONIVEL
    #                         (body: {"message":"Content Not Found"} ou similar)
    #     HTTP 429         →  rate limit               → RATELIMIT
    #
    #   A versao antiga tentava detectar "not found" no body do 400, mas o
    #   TikTok nao manda essa string — manda "Content Not Found" ou nada.
    #   Como nenhum dos if batia, todos os 400 viravam 'taken', fazendo
    #   todos os nomes aparecerem como indisponiveis.
    #
    #   FIX: username valido + HTTP 400 = DISPONIVEL (sem checar o body).
    #        Validamos o username ANTES de fazer o request para descartar
    #        formatos invalidos que tambem retornam 400.
    #
    # ─────────────────────────────────────────────────────────────────────────

    def _check(self, username, proxy=None):
        if not is_valid_tt_username(username):
            return 'invalid'

        try:
            r = requests.get(
                'https://www.tiktok.com/oembed',
                params={'url': f'https://www.tiktok.com/@{username}'},
                headers={
                    'User-Agent'     : random.choice(self._UAS),
                    'Accept'         : 'application/json',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer'        : 'https://www.tiktok.com/',
                },
                proxies=proxy, timeout=10, verify=False
            )

            # HTTP 200: perfil existe → TOMADO
            if r.status_code == 200:
                try:
                    j = r.json()
                    if j.get('author_name') or j.get('author_url') or j.get('title'):
                        return 'taken'
                except Exception:
                    pass
                return 'taken'

            # HTTP 400/404: perfil nao existe OU reservado/banido.
            # Usamos User Detail API + HTML check conservador.
            if r.status_code in (400, 404):
                return self._api_detail_check(username, proxy)

            # HTTP 429: rate limit
            if r.status_code == 429:
                with self.lock: self.Rl += 1
                return 'ratelimit'

            return 'error'

        except requests.exceptions.ProxyError as e:
            return 'proxy_error'
        except requests.exceptions.Timeout:
            return 'proxy_error' if proxy else 'error'
        except requests.exceptions.RequestException:
            return 'error'
        except Exception:
            return 'error'

    def _api_detail_check(self, username, proxy=None):
        """
        TikTok User Detail API — verifica via endpoint interno sem autenticacao.

        GET https://www.tiktok.com/api/user/detail/?uniqueId={user}&aid=1988

        Respostas:
          statusCode: 0  + userInfo com uniqueId → TOMADO (conta ativa)
          statusCode: 10202 → usuario nao encontrado (mas pode ser reservado)
          statusCode: 10221 → username reservado pelo TikTok → TOMADO
          Timeout / erro → faz fallback para html_check conservador

        Para distinguir reservado (10202 mas nao registravel) de livre:
          Verifica TAMBÉM a pagina @username buscando sinais de reserva.
        """
        ua = random.choice(self._UAS)
        proxy_dict = self._build_proxy(proxy) if proxy else None

        # ── Step 1: User detail API ────────────────────────────────────────
        try:
            r = requests.get(
                'https://www.tiktok.com/api/user/detail/',
                params={
                    'uniqueId': username,
                    'aid':      '1988',
                    'count':    '30',
                    'cursor':   '0',
                },
                headers={
                    'User-Agent'     : ua,
                    'Accept'         : 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer'        : f'https://www.tiktok.com/@{username}',
                },
                proxies=proxy_dict, timeout=10, verify=False
            )

            if r.status_code == 429:
                with self.lock: self.Rl += 1
                return 'ratelimit'

            if r.status_code == 200:
                try:
                    j = r.json()
                    sc = j.get('statusCode', j.get('status_code', -1))

                    if sc == 0:
                        # active account found
                        return 'taken'

                    if sc in (10221, 10222, 10223):
                        # reserved / suspended / banned username
                        return 'taken'

                    if sc == 10202:
                        # "user not found" — could be truly free OR reserved
                        # do html_check as tiebreaker
                        return self._html_check_conservative(username, proxy_dict)

                    # any other status → conservative: taken
                    return 'taken'

                except Exception:
                    pass

        except requests.exceptions.Timeout:
            pass
        except Exception:
            pass

        # ── Step 2: Fallback to conservative HTML check ────────────────────
        return self._html_check_conservative(username, proxy_dict)

    def _html_check_conservative(self, username, proxy=None):
        """
        Verifica a pagina de perfil com logica conservadora.

        Nomes RESERVADOS pelo TikTok (como plat0, obrai, auchw, 8iles):
          - A pagina retorna HTTP 200
          - O titulo da pagina e apenas "TikTok" (sem username)
          - NAO ha uniqueId no HTML
          - statusCode pode ser 10202 mas NAO ha texto "not found"
          - O TikTok sugere variacoes: "plat01", "plat02" (sinal de reserva)

        Username REALMENTE LIVRE:
          - HTTP 404, OU
          - HTTP 200 + titulo "TikTok" + texto explicito de "not found"
        
        Logica: qualquer 200 sem texto de "not found" = TOMADO (conservador).
        """
        import json as _json, re as _re2
        try:
            r = requests.get(
                f'https://www.tiktok.com/@{username}',
                headers={
                    'User-Agent'     : random.choice(self._UAS),
                    'Accept'         : 'text/html,application/xhtml+xml',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer'        : 'https://www.tiktok.com/',
                },
                proxies=proxy, timeout=10, verify=False, allow_redirects=True
            )

            if r.status_code == 404:
                return 'available'
            if r.status_code != 200:
                return 'taken'

            body = r.text
            body_low = body.lower()
            ulow = username.lower()

            # ── Taken signals: active or reserved account ─────────────────
            for sig in [f'"uniqueid":"{ulow}"', '"followercount"',
                        '"heartcount"', '"videocount"', '"authorstats"',
                        '"privateaccount"']:
                if sig in body_low:
                    return 'taken'

            # ── Check page title: active="@user | TikTok", reserved/404="TikTok" ──
            title_match = _re2.search(r'<title>([^<]+)</title>', body)
            if title_match:
                title = title_match.group(1).strip().lower()
                # If title contains the username → active account
                if ulow in title:
                    return 'taken'

            # ── SIGI_STATE analysis ───────────────────────────────────────
            sigi_match = _re2.search(r'SIGI_STATE[^>]*>({.+?})</script>', body, _re2.DOTALL)
            if sigi_match:
                try:
                    sigi = _json.loads(sigi_match.group(1))

                    # statusCode 0 = active account
                    if sigi.get('statusCode', -1) == 0:
                        return 'taken'

                    # Look for userInfo — if present and has uniqueId → taken
                    # If present but empty {} → RESERVED (plat0, obrai style)
                    for key in ['UserDetail','userDetail','UserPage','userPage']:
                        ud = sigi.get(key, {})
                        ui = ud.get('userInfo', ud.get('user_info', None))
                        if ui is not None:
                            if ui == {} or ui == {'user':{}, 'stats':{}}:
                                # empty userInfo = RESERVED slot
                                return 'taken'
                            if ui.get('user', {}).get('uniqueId'):
                                return 'taken'

                    # statusCode 10202 in SIGI
                    sc = sigi.get('statusCode', sigi.get('status_code', -1))
                    if sc == 10202:
                        # Only mark available if we see explicit not-found text
                        not_found = [
                            "couldn't find this account",
                            "this account doesn't exist",
                            "couldn't find", "not found"
                        ]
                        if any(p in body_low for p in not_found):
                            return 'available'
                        # 10202 but NO "not found" text → RESERVED
                        return 'taken'
                except Exception:
                    pass

            # ── No SIGI or statusCode found ───────────────────────────────
            # If page loaded (200) but no profile signals AND no "not found" text
            # → Could be reserved. Check for explicit not-found text.
            not_found_phrases = [
                "couldn't find this account",
                "this account doesn't exist", 
                "couldn't find",
                "not found",
                "does not exist",
            ]
            if any(p in body_low for p in not_found_phrases):
                return 'available'

            # 200 + no signals + no "not found" → RESERVED/TAKEN (conservative)
            return 'taken'

        except Exception:
            return 'taken'

    def _html_check(self, username, proxy=None):
        """
        Double-check via pagina de perfil para nomes curtos (<= 4 chars).
        O TikTok embute SIGI_STATE JSON no HTML com dados do usuario.

        Se encontrar "uniqueId":"username" no HTML → username EXISTE (reservado/banido/ativo) → TOMADO
        Se encontrar statusCode 10202 → nao existe → DISPONIVEL
        Se nao conseguir determinar → TOMADO (seguro para nomes curtos)
        """
        try:
            r = requests.get(
                f'https://www.tiktok.com/@{username}',
                headers={
                    'User-Agent'     : random.choice(self._UAS),
                    'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer'        : 'https://www.tiktok.com/',
                },
                proxies=proxy, timeout=12, verify=False, allow_redirects=True
            )

            body = r.text.lower()
            ulow = username.lower()

            # Sinais de que o username EXISTE (reservado, banido ou ativo)
            taken_signals = [
                f'"uniqueid":"{ulow}"',
                f'"uniqueId":"{ulow}"',
                '"authorstats"',
                '"usermeta"',
                '"privateaccount"',
            ]
            for sig in taken_signals:
                if sig.lower() in body:
                    return 'taken'

            # Sinal de que o username NAO existe
            if '"statuscode":10202' in body or '"status_code":10202' in body:
                return 'available'

            # Nao conseguiu determinar → conservador: TOMADO
            return 'taken'

        except Exception:
            return 'taken'  # em caso de erro no double-check, nao reporta como disponivel

    # ── webhook / hits ────────────────────────────────────────────────────────

    def _send_webhook(self, username):
        """Envia webhook em thread separada."""
        if not self.webhook: return
        msg = self._L['wh_msg'].format(username)

        def _send():
            try:
                r = requests.post(self.webhook, json={'content': msg}, timeout=8)
                if r.status_code == 429:
                    retry = float(r.json().get('retry_after', 1))
                    time.sleep(retry)
                    requests.post(self.webhook, json={'content': msg}, timeout=8)
            except Exception:
                pass

        threading.Thread(target=_send, daemon=True).start()

    def _on_available(self, username):
        with self.lock: self.available += 1; self.att += 1
        if self.save_hits:
            try:
                with open(BOT_HITS_FILE, 'a', encoding='utf-8') as f:
                    f.write(username + '\n')
            except Exception: pass
        print(f'\r\033[K' + self._L['avail'].format(username))
        self._send_webhook(username)

    def _on_taken(self, username):
        with self.lock: self.att += 1
        print(f'\r' + self._L['taken'].format(username) + '\033[K', end='', flush=True)

    # ── printer ───────────────────────────────────────────────────────────────

    def _printer(self):
        while self.go:
            with self.lock:
                u  = '...'
                rl = 0
                for st in self.thread_status.values():
                    if st.get('username'): u = st['username']
                    if st.get('rl', 0) > time.time(): rl = st['rl']
            if rl > 0:
                rem = max(0, int(rl - time.time()))
                print(f'\r' + self._L['rl'].format(rem) + '\033[K', end='', flush=True)
            else:
                print(f'\r' + self._L['checking'].format(u) + '\033[K', end='', flush=True)
            time.sleep(0.3)

    # ── modo classico ─────────────────────────────────────────────────────────

    def _run_classic(self):
        self.thread_status[0] = {'username': '...', 'status': 'iniciando', 'rl': 0}

        try:
            while self.go:
                username = self._gen_username()
                if not username: time.sleep(0.1); continue
                self._set_status(0, username=username, status='verificando', rl=-1)

                proxy_raw = self._next_proxy_raw() if self.using_proxy else None
                result = self._check(username, self._build_proxy(proxy_raw))

                if result == 'available':
                    self._set_status(0, status='available')
                    self._on_available(username)
                elif result == 'taken':
                    self._set_status(0, status='nao disponivel')
                    self._on_taken(username)
                elif result == 'ratelimit':
                    if proxy_raw:
                        self._mark_proxy_rl(proxy_raw, 120)
                        self._log('RL', f'proxy={proxy_raw} RL 120s — trocando')
                    else:
                        self._log('RL', 'Sem proxy RL 120s — aguardando...')
                        self._set_status(0, rl=120)
                        time.sleep(120)
                        self._set_status(0, rl=-1, status='verificando')
                elif result == 'proxy_error':
                    self._kill_proxy(proxy_raw)
                    self._set_status(0, status='proxy morta')
                elif result == 'invalid':
                    self._set_status(0, status='invalido')
                else:
                    if proxy_raw: self._kill_proxy(proxy_raw)
                    time.sleep(2)

        except KeyboardInterrupt:
            self.go = False

    # ── modo threaded ─────────────────────────────────────────────────────────

    def _run_threaded(self):
        name_queue = queue.Queue(maxsize=self.n_threads * 4)

        def feeder():
            while self.go:
                u = self._gen_username()
                if u:
                    try: name_queue.put(u, timeout=1)
                    except queue.Full: pass
                else:
                    time.sleep(0.1)

        threading.Thread(target=feeder, daemon=True).start()

        def worker(wid):
            self._set_status(wid, username='...', status='aguardando', rl=-1)

            while self.go:
                try: username = name_queue.get(timeout=2)
                except queue.Empty: continue

                self._set_status(wid, username=username, status='verificando', rl=-1)
                proxy_raw = self._next_proxy_raw() if self.using_proxy else None
                result = self._check(username, self._build_proxy(proxy_raw))

                if result == 'available':
                    self._set_status(wid, status='available')
                    self._on_available(username)

                elif result == 'taken':
                    self._set_status(wid, status='nao disponivel')
                    self._on_taken(username)

                elif result == 'ratelimit':
                    if proxy_raw:
                        self._mark_proxy_rl(proxy_raw, 120)
                        self._log('RL', f'W{wid} proxy={proxy_raw} RL 120s')
                        try: name_queue.put_nowait(username)
                        except queue.Full: pass
                    else:
                        self._log('RL', f'W{wid} sem proxy RL 120s')
                        self._set_status(wid, username=username, rl=120)
                        time.sleep(120)
                        self._set_status(wid, rl=-1, status='verificando')
                        try: name_queue.put_nowait(username)
                        except queue.Full: pass

                elif result == 'proxy_error':
                    self._kill_proxy(proxy_raw)
                    self._set_status(wid, status='proxy morta')
                    try: name_queue.put_nowait(username)
                    except queue.Full: pass

                elif result == 'invalid':
                    self._set_status(wid, status='invalido')

                else:
                    if proxy_raw: self._kill_proxy(proxy_raw)
                    try: name_queue.put_nowait(username)
                    except queue.Full: pass
                    time.sleep(1)

                name_queue.task_done()

        for i in range(1, self.n_threads + 1):
            threading.Thread(target=worker, args=(i,), daemon=True).start()

        self._log('THREADS', f'{self.n_threads} threads iniciadas')

        try:
            while self.go: time.sleep(1)
        except KeyboardInterrupt:
            self.go = False


if __name__ == '__main__':
    init(autoreset=True)
    TikTokChecker()
