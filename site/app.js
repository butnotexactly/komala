var tooltipElement,
    arrowElement,
    titleElement,
    descElement,
    thumbElement,
    dexElement,
    fieldsElement;

var nodes;
var viewing = null;

document.addEventListener('DOMContentLoaded', function(e) {
    tooltipElement = document.querySelector('#tt');
    arrowElement = document.querySelector('#tt_arrow');
    titleElement = document.querySelector('#tt_title');
    descElement = document.querySelector('#tt_desc');
    thumbElement = document.querySelector('#tt_thumb');
    dexElement = document.querySelector('#tt_dex');
    fieldsElement = document.querySelector('#tt_fields');

    nodes = [
        document.querySelector('#world_img_0'),
        document.querySelector('#world_img_1'),
        document.querySelector('#world_img_2'),
        document.querySelector('#world_img_3'),
        document.querySelector('#world_img_4'),
    ];
});

document.addEventListener('mouseover', function(e) {
    var no = e.target.dataset.no;
    if (typeof no !== 'undefined')
    {
        if(!viewing || viewing != no)
        {
            viewing = no;
            loadTooltip(no);

            var w = tooltipElement.offsetWidth;
            var h = tooltipElement.offsetHeight;

            if (e.target.offsetLeft + 90 + w + 30 < document.documentElement.clientWidth)
            {
                tooltipElement.style.left = (e.target.offsetLeft + 90) + 'px';
                tooltipElement.style.top = (e.target.offsetTop - h / 2 + 40) + 'px';
                tooltipElement.className = 'tooltip bs-tooltip-right';
            }
            else if (e.target.offsetLeft - w - 30 > 0)
            {
                tooltipElement.style.left = (e.target.offsetLeft - w - 10) + 'px';
                tooltipElement.style.top = (e.target.offsetTop - h / 2 + 40) + 'px';
                tooltipElement.className = 'tooltip bs-tooltip-left';
            }
            else
            {
                var bodyRect = document.body.getBoundingClientRect(),
                    targetRect = e.target.getBoundingClientRect(),
                    offset = targetRect.top - bodyRect.top;
                if(offset < document.documentElement.scrollTop + document.documentElement.clientHeight / 2)
                {
                    tooltipElement.style.left = (e.target.offsetLeft - w / 2 + 40) + 'px';
                    tooltipElement.style.top =  (e.target.offsetTop + 90) + 'px';
                    tooltipElement.className = 'tooltip bs-tooltip-bottom';
                }
                else
                {
                    tooltipElement.style.left = (e.target.offsetLeft - w / 2 + 40) + 'px';
                    tooltipElement.style.top =  (e.target.offsetTop - h - 10) + 'px';
                    tooltipElement.className = 'tooltip bs-tooltip-top';
                }
            }

            tooltipElement.style.opacity = 1;

            // console.log('st: ' +((window.pageYOffset || document.documentElement.scrollTop)  - (document.documentElement.clientTop || 0)));
            // console.log('st2: ' + document.documentElement.scrollTop);
            // //console.log('ch: ' +document.documentElement.scrollHeight);
            // console.log('')

        }
    }
    else
    {
        viewing = null;
        tooltipElement.style.opacity = 0;
    }
});

function loadTooltip(n) {
    titleElement.innerText = dict[n]['name'];
    descElement.innerHTML = dict[n]['desc'];
    dexElement.innerHTML = dict[n]['bio'];
    thumbElement.src = '';
    thumbElement.src = dict[n]['thumb'];

    var fields = dict[n]['fields'];
    var fieldsHtml = '';
    for (var i = 0; i < fields.length; i++) {
        fieldsHtml +=
            '<div class="field">\n' +
            '    <div class="name">' + fields[i]['name'] + '</div>\n' +
            '    <div class="value">' + fields[i]['value'].replace(/<br><br>/g, '<br>') + '</div>\n' +
            '</div>\n';
    }
    fieldsElement.innerHTML = fieldsHtml;
}


var nodeIndex = 0;
var queuePosition = -1;
var queue;
setTimeout(function() { setInterval(loadNextImage, 2000); }, 1000);

function loadNextImage() {
    var node;// = nodes[nodeIndex];
    while(!node || node.style.display == 'none')
        node = nodes[Math.floor(Math.random() * nodes.length)]

    if(queuePosition == -1 || queuePosition >= queue.length) {
        queuePosition = 0;
        queue = sample(60, 0, world.length);
    }

    loadImageOntoNode(node, queue[queuePosition]);
    queuePosition++;
    // nodeIndex++;
    // if(nodeIndex >= nodes.length || nodes[nodeIndex].style.display == 'none')
    //     nodeIndex = 0;
}

function loadImageOntoNode(node, i) {
    var next = document.createElement('img');
    next.onload = function() {
        node.src = this.src;
    };
    next.src = world[i][1];
}

var world = [
    ['Outdoors', 'https://i.imgur.com/eu55aWZ.png'],
    // ["Oak's Lab", 'https://i.imgur.com/U2Ok0FL.png'],
    ['North', 'https://i.imgur.com/XtahuoV.png'],
    ['South', 'https://i.imgur.com/3hZeLhX.png'],
    ['Crossing', 'https://i.imgur.com/NoRh19C.png'],
    ['Downtown', 'https://i.imgur.com/FbCCGUo.png'],
    ['Pond', 'https://i.imgur.com/CtNbZGi.png'],
    ['Pokémon Center', 'https://i.imgur.com/c6HZFZz.png'],
    ["Warden's Home", 'https://i.imgur.com/KSzEjq3.png'],
    ['Greenhouse', 'https://i.imgur.com/2TF6hm5.png'],
    ['Hilltop', 'https://i.imgur.com/XcAEkao.png'],
    ["Angler's Point", 'https://i.imgur.com/WniTRCC.png'],
    ['Garden Maze', 'https://i.imgur.com/p9iyf24.png'],
    ['Ascent', 'https://i.imgur.com/xtZCNY3.png'],
    ['Bidoof Bridge', 'https://i.imgur.com/YGChhO4.png'],
    ['Lake Center', 'https://i.imgur.com/HyDedxH.png'],
    ['Entrance (East)', 'https://i.imgur.com/aJZUzVF.png'],
    ['Tranquil Corner', 'https://i.imgur.com/SK7fxgI.png'],
    ['Entrance (South)', 'https://i.imgur.com/1KN0uxR.png'],
    ['Poliwag Nest', 'https://i.imgur.com/MJZatvn.png'],
    ['Tropics', 'https://i.imgur.com/ZbcB13F.png'],
    ['Palm Trees', 'https://i.imgur.com/OSHdnNs.png'],
    ['Coconut Cabanas', 'https://i.imgur.com/7DrLjYc.png'],
    ['Beach Walkway', 'https://i.imgur.com/oFy14Y2.png'],
    ['Sandshrew Sands', 'https://i.imgur.com/yKezNYU.png'],
    ['Hammocks', 'https://i.imgur.com/ZoF6xE7.png'],
    ['Sandcastle Spot', 'https://i.imgur.com/9R2KIS1.png'],
    ['Coastline', 'https://i.imgur.com/L76xJen.png'],
    ['Dunes', 'https://i.imgur.com/YARgbgU.png'],
    ['Isles', 'https://i.imgur.com/OXpvQcK.png'],
    ['Deep Sea', 'https://i.imgur.com/pFmAthF.png'],
    ['Rocky Waters', 'https://i.imgur.com/nvp6PhE.png'],
    ['Flower Forest', 'https://i.imgur.com/cb7HEjw.png'],
    ['Fairy Bridge', 'https://i.imgur.com/fWApPeC.png'],
    ['Waterside Cliffs', 'https://i.imgur.com/o4VINEz.png'],
    ['Air Lift', 'https://i.imgur.com/E3qYGok.png'],
    ["Trail's End", 'https://i.imgur.com/3uexCjr.png'],
    ['New Trainer Alley', 'https://i.imgur.com/JUD5sGU.png'],
    ['Swamp Edge', 'https://i.imgur.com/gfZfBwg.png'],
    ['Trail Fork', 'https://i.imgur.com/YL8jmQX.png'],
    ['City Entrance', 'https://i.imgur.com/PkdoZ1l.png'],
    ['Toxic Pools', 'https://i.imgur.com/6Kvzpg4.png'],
    ['Forest Hollows', 'https://i.imgur.com/N6Di19C.png'],
    ['Marshland', 'https://i.imgur.com/9DqeNhk.png'],
    ['Boardwalk Bog', 'https://i.imgur.com/vxQHRMN.png'],
    ['Off the beaten path...', 'https://i.imgur.com/oNUOnSv.png'],
    ['Temple Entrance', 'https://i.imgur.com/34Zmiz1.png'],
    ['Mangroves', 'https://i.imgur.com/IjiyOdf.png'],
    ['Village Entrance', 'https://i.imgur.com/E8hWlQS.png'],
    ['Village Huts', 'https://i.imgur.com/Jx8mPn0.png'],
    ['Wildlands', 'https://i.imgur.com/Gu59QT5.png'],
    ['Quagmire', 'https://i.imgur.com/PnbYnKN.png'],
    // ['Class S', 'https://i.imgur.com/uNNPHos.png'],
    ['Leader', 'https://i.imgur.com/J7hRLWD.png'],
    ['Class A', 'https://i.imgur.com/WfOfhGJ.png'],
    ['Class B', 'https://i.imgur.com/TPAHagd.png'],
    // ['Anteroom', 'https://i.imgur.com/Xq1llpg.png'],
    // ['Class C', 'https://i.imgur.com/T70jLH9.png'],
    ['Crest', 'https://i.imgur.com/Boz7ths.png'],
    ['Statue', 'https://i.imgur.com/3aBVV5u.png'],
    ['Temple Summit', 'https://i.imgur.com/JISH7BL.png'],
    ['Eastern Temple', 'https://i.imgur.com/B3WNRnN.png'],
    ['A Calm Respite', 'https://i.imgur.com/pUnfM63.png'],
    ['Temple Grounds', 'https://i.imgur.com/X524dzw.png'],
    ['Lilywater', 'https://i.imgur.com/woqBsiq.png'],
    ['Sunflower Field', 'https://i.imgur.com/uXtdleR.png'],
    ['Riverside', 'https://i.imgur.com/VkAX2rQ.png'],
    ['Rainbow Orchard', 'https://i.imgur.com/poT9Qcy.png'],
    ['Bridge', 'https://i.imgur.com/WO4PCyP.png'],
    ['Sky Caverns', 'https://i.imgur.com/ZMKvhmc.png'],
    ['Altaria Falls', 'https://i.imgur.com/An5tLEX.png'],
    ['Dropoff', 'https://i.imgur.com/LXu1U9T.png'],
    ['Fairy Falls', 'https://i.imgur.com/FMHqt1H.png'],
    ['Island Rapids', 'https://i.imgur.com/UL8qw60.png'],
    ['Cloudy Climb', 'https://i.imgur.com/gyfwKV4.png'],
    ['White Sea', 'https://i.imgur.com/HdfexmI.png'],
    ['Landing', 'https://i.imgur.com/2zNXWKb.png'],
    ['Island Hopping', 'https://i.imgur.com/xoHjICC.png'],
    ['Tech District', 'https://i.imgur.com/f4Jpkkw.png'],
    ['City Center', 'https://i.imgur.com/1VfXHI0.png'],
    ['Mareep Meadows', 'https://i.imgur.com/C1j9IFJ.png'],
    ['Chinchou Falls', 'https://i.imgur.com/r06OP4C.png'],
    ['Docks', 'https://i.imgur.com/hyUcsGm.png'],
    ['City Crossing', 'https://i.imgur.com/BF0CgUs.png'],
    ['Power Plant', 'https://i.imgur.com/23A73zw.png'],
    ['Construction Yard', 'https://i.imgur.com/8JOtZZr.png'],
    ["???'s Cabin", 'https://i.imgur.com/xC2ez8J.png'],
    ['Flaafy Forest', 'https://i.imgur.com/mINXqJc.png'],
    ['Downtown', 'https://i.imgur.com/0Kj2Q3N.png'],
    ['Market Street', 'https://i.imgur.com/Zy2fVH6.png'],
    ['Boulder Point', 'https://i.imgur.com/5n5wAbQ.png'],
    ['City Outskirts', 'https://i.imgur.com/OEjOBkz.png'],
    ['First Snow', 'https://i.imgur.com/lSyxtwT.png'],
    ['Hike Start', 'https://i.imgur.com/v9OuXGw.png'],
    ['Nidoran Nest', 'https://i.imgur.com/miFDo23.png'],
    ['Ascent', 'https://i.imgur.com/hCEtwHt.png'],
    // ['Cave Tunnel', 'https://i.imgur.com/3uLOMqd.png'],
    // ['Climb', 'https://i.imgur.com/3PCTRkj.png'],
    // ['Ice Fossils', 'https://i.imgur.com/0a1tqxT.png'],
    // ['Pewter Entrance', 'https://i.imgur.com/dCEUnFB.png'],
    // ['Vanillite Stalagmites', 'https://i.imgur.com/Jlzagxt.png'],
    // ['Bergmite Stalactites', 'https://i.imgur.com/O0GxLGo.png'],
    // ['Cubchoo Den', 'https://i.imgur.com/mQGspf9.png'],
    // ['Swinub Nest', 'https://i.imgur.com/o03YhaW.png'],
    // ['Spheal Sanctuary', 'https://i.imgur.com/XaMPBEt.png'],
    // ['A Frozen Respite', 'https://i.imgur.com/amXADS6.png'],
    // ["Snow's Secret", 'https://i.imgur.com/jQVlhqS.png'],
    // ['Frosty Slide', 'https://i.imgur.com/kAzwz3T.png'],
    // ['Last Stretch', 'https://i.imgur.com/KZIR4ag.png'],
    // ['North Face', 'https://i.imgur.com/2pdXUnB.png'],
    // ['Christmas Entrance', 'https://i.imgur.com/EGzY0zi.png'],
    ['Winter Park', 'https://i.imgur.com/3lFjoP6.png'],
    ['Downtown', 'https://i.imgur.com/Ebsr5uU.png'],
    ['Grand Christmas Tree', 'https://i.imgur.com/fjUdpNi.png'],
    ['Alleyway', 'https://i.imgur.com/r2reXSa.png'],
    ["???'s House", 'https://i.imgur.com/DwyNfE9.png'],
    ['Delibird Lake', 'https://i.imgur.com/Lmj6VDQ.png'],
    ['Pleasant Path', 'https://i.imgur.com/q42QVaG.png'],
    ['Village Corner', 'https://i.imgur.com/J8mRW71.png'],
    // ['Dropdown', 'https://i.imgur.com/mjTlNlr.png'],
    // ["Titan's Domain", 'https://i.imgur.com/NB1A3XH.png'],
    ['Cozy Corner', 'https://i.imgur.com/PQOxD1N.png'],
    ['Northpoint', 'https://i.imgur.com/AXJYz13.png'],
    ['Frosty Forest', 'https://i.imgur.com/F1PLVbq.png'],
    ['The Highest Gym', 'https://i.imgur.com/gsNtmT3.png'],
    ['Snover Trees', 'https://i.imgur.com/RCe6rrm.png'],
    ['Snowy Pass', 'https://i.imgur.com/rmGI0JF.png'],
    ['Snow Valley', 'https://i.imgur.com/qI7mSlC.png'],
    ['2F', 'https://i.imgur.com/UD4UE5Z.png'],
    ['1F', 'https://i.imgur.com/D4HBmZB.png'],
    ['Peak', 'https://i.imgur.com/oMCZWkP.png'],
    ['Descent', 'https://i.imgur.com/Eyzu4D8.png'],
    ['Mine Entrance', 'https://i.imgur.com/6PkBIUh.png'],
    ['Ghost Valley', 'https://i.imgur.com/pt0UlDI.png'],
    ['Rustic Homes', 'https://i.imgur.com/i0gIoCd.png'],
    ['Whitegrass', 'https://i.imgur.com/E85TZgr.png'],
    // ['Clocktower 2F', 'https://i.imgur.com/OUH8FE3.png'],
    // ['Clocktower 1F', 'https://i.imgur.com/JXMgx6A.png'],
    ['3F Litwick Waxtone', 'https://i.imgur.com/ZRniMtc.png'],
    ['2F An eerie sensation...', 'https://i.imgur.com/FDu2f5G.png'],
    ['1F Whiteout', 'https://i.imgur.com/5URTKBT.png'],
    ['2F Spirit Gathering', 'https://i.imgur.com/0nIUYJ6.png'],
    ['Wilderness', 'https://i.imgur.com/uBF3svM.png'],
    ['Fearow Camp', 'https://i.imgur.com/Nuv3CPp.png'],
    ['Mountainside', 'https://i.imgur.com/qmYvYmS.png'],
    ['Old Bridge', 'https://i.imgur.com/My1DefV.png'],
    ['Murkrow Elm', 'https://i.imgur.com/ifz6bdz.png'],
    ['Scary Woods', 'https://i.imgur.com/vfAlpZR.png'],
    ['Fungi Patch', 'https://i.imgur.com/MVKVx9Z.png'],
    ['Pancham Pass', 'https://i.imgur.com/IrEdTLx.png'],
    ['Forest Depths', 'https://i.imgur.com/TyUPzsv.png'],
    ['Labyrinth', 'https://i.imgur.com/0gxNwjY.png'],
    ['Forest Edge', 'https://i.imgur.com/KmihC9A.png'],
    ['City Opening', 'https://i.imgur.com/jetMwJJ.png'],
    ['Winding Trail', 'https://i.imgur.com/5vDCVwZ.png'],
    ['Black Pond', 'https://i.imgur.com/fuKTGwq.png'],
    ['Shiftry Trees', 'https://i.imgur.com/NDwSR4M.png'],
    ['Outskirts', 'https://i.imgur.com/d4GFqf4.png'],
    ['Pokémon Institute', 'https://i.imgur.com/7uExDn3.png'],
    ['Residences', 'https://i.imgur.com/r7Tx9wB.png'],
    ['West Exit', 'https://i.imgur.com/CEyaGQh.png'],
    ['City Fountain', 'https://i.imgur.com/fAnatKp.png'],
    ['East Exit', 'https://i.imgur.com/htK7JKr.png'],
    ['Side Street', 'https://i.imgur.com/3MSAVaJ.png'],
    ['Market Street', 'https://i.imgur.com/rbeXeBd.png'],
    ['Finance District', 'https://i.imgur.com/RVJuevZ.png'],
    ['Backalley', 'https://i.imgur.com/MvNpcAn.png'],
    ['South Exit', 'https://i.imgur.com/MrPG6lR.png'],
    ["???'s House", 'https://i.imgur.com/vpwO1HM.png'],
    ['Shore', 'https://i.imgur.com/ZD2OckJ.png'],
    ['Rockline', 'https://i.imgur.com/SI3UGfQ.png'],
    ['West Cavern', 'https://i.imgur.com/54xhOqu.png'],
    ['Gym Tunnel', 'https://i.imgur.com/3wWp1AE.png'],
    ['East Cavern', 'https://i.imgur.com/G7565sP.png'],
    ['Lapras Den', 'https://i.imgur.com/FX82vbu.png'],
    ['Channel', 'https://i.imgur.com/yE1HEVH.png'],
    ['Algae Farm', 'https://i.imgur.com/LyEyqIv.png'],
    // ['Sea Passage', 'https://i.imgur.com/gE0ryo9.png'],
    // ['Corsola Corals', 'https://i.imgur.com/kGynehj.png'],
    // ['Sea Passage', 'https://i.imgur.com/GsP2hGJ.png'],
    // ['Crags', 'https://i.imgur.com/vP8e7Dy.png'],
    // ['Great Sea Crevice', 'https://i.imgur.com/hf0VurJ.png'],
    // ['Abyss Edge', 'https://i.imgur.com/fU86ZHw.png'],
    // ['Horsea Nest', 'https://i.imgur.com/QcfcTBu.png'],
    // ['Still Waters', 'https://i.imgur.com/AxY0dMS.png'],
    // ['Deep Sea', 'https://i.imgur.com/G6OPRk1.png'],
    ['Waterside Cliffs', 'https://i.imgur.com/b9J1wVh.png'],
    ['Isle', 'https://i.imgur.com/eEmayBX.png'],
    ['Mt. Sulfur', 'https://i.imgur.com/Pdkg3pf.png'],
    ['Ridgeline', 'https://i.imgur.com/kEQlir9.png'],
    ['Surface', 'https://i.imgur.com/s2G2zBw.png'],
    ['East Shore', 'https://i.imgur.com/74JAq1N.png'],
    ['Lush Trail', 'https://i.imgur.com/1nHotf6.png'],
    ['South Shore', 'https://i.imgur.com/EOHnZDS.png'],
    ['Sandy Dunes', 'https://i.imgur.com/rP6n77H.png'],
    ['Downtown', 'https://i.imgur.com/e80SyyD.png'],
    ['Mt. Cinder Entrance', 'https://i.imgur.com/LkZZtgG.png'],
    ['Pokémon Gym', 'https://i.imgur.com/662Aznz.png'],
    ['City of Dragons', 'https://i.imgur.com/jL2jKBC.png'],
    ['Mountain Grassland', 'https://i.imgur.com/2TKZPTG.png'],
    ['Crag Forest', 'https://i.imgur.com/B9FihFR.png']
];

var dict = {
    1: {
        name: "Bulbasaur",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Bulbasaur can be seen napping in bright sunlight. There is a seed on its back. By soaking up the sun's rays, the seed grows progressively larger.",
        footer: "Tier 1 • [35-80%] • No. 1 / Base Set 1",
        img: "https://i.imgur.com/yL1EUoX.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/bulbasaur.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Vine Whip',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em><br><br><strong>3</strong>% 🌱 Leech Seed Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/water.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/nature.png">'
            }
        ]
    },
    2: {
        name: "Ivysaur",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "When the bulb on its back grows large, it appears to lose the ability to stand on its hind legs.",
        footer: "Tier 2 • [55-100%] • No. 2 / Base Set 1",
        img: "https://i.imgur.com/U5fNtCb.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/ivysaur.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Razor Leaf',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em><br><br><strong>3</strong>% 🌱 Leech Seed Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/water.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/nature.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/nature.png">'
            }
        ]
    },
    3: {
        name: "Venusaur",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "By spreading the broad petals of its flower and catching the sun's rays, it fills its body with power.",
        footer: '',
        img: "https://i.imgur.com/OY6pACI.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/venusaur.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    4: {
        name: "Mega Venusaur",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "The plant blooms when it is absorbing solar energy. It stays on the move to seek sunlight.",
        footer: '',
        img: "https://i.imgur.com/7AwYQdH.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/venusaur-mega.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    5: {
        name: "Charmander",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "The flame that burns at the tip of its tail is an indication of its emotions. The flame wavers when Charmander is enjoying itself. If the Pokémon becomes enraged, the flame burns fiercely.",
        footer: "Tier 1 • [35-80%] • No. 4 / Base Set 1",
        img: "https://i.imgur.com/1DLtust.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/charmander.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Ember',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em><br><br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/fire.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/nature.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/fire.png">'
            }
        ]
    },
    6: {
        name: "Charmeleon",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Charmeleon mercilessly destroys its foes using its sharp claws. If it encounters a strong foe, it turns aggressive. In this excited state, the flame at the tip of its tail flares with a bluish white color.",
        footer: "Tier 2 • [55-100%] • No. 5 / Base Set 1",
        img: "https://i.imgur.com/g2BzIPH.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/charmeleon.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Flamethrower',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em><br><br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/fire.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/nature.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/fire.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/fire.png">'
            }
        ]
    },
    7: {
        name: "Charizard",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Charizard flies around the sky in search of powerful opponents. It breathes fire of such great heat that it melts anything. However, it never turns its fiery breath on any opponent weaker than itself.",
        footer: '',
        img: "https://i.imgur.com/QyIPHR5.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/charizard.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    9: {
        name: "Mega Charizard Y",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Charizard flies around the sky in search of powerful opponents. It breathes fire of such great heat that it melts anything. However, it never turns its fiery breath on any opponent weaker than itself.",
        footer: '',
        img: "https://i.imgur.com/sm7QEnB.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/charizard-megay.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    8: {
        name: "Mega Charizard X",
        desc: '<img class="icon" src="images/types/dragon.png">Dragon Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png">',
        bio: "Charizard flies around the sky in search of powerful opponents. It breathes fire of such great heat that it melts anything. However, it never turns its fiery breath on any opponent weaker than itself.",
        footer: '',
        img: "https://i.imgur.com/RPBmMZe.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/charizard-megax.gif",
        type: 10,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    10: {
        name: "Squirtle",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Squirtle’s shell is not merely used for protection. The shell’s rounded shape and the grooves on its surface help minimize resistance in water, enabling this Pokémon to swim at high speeds.",
        footer: "Tier 1 • [35-80%] • No. 7 / Base Set 1",
        img: "https://i.imgur.com/eBRhc94.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/squirtle.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Water Gun',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em>"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/water.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/fire.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/water.png">'
            }
        ]
    },
    11: {
        name: "Wartortle",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Its tail is large and covered with a rich, thick fur. The tail becomes increasingly deeper in color as Wartortle ages. The scratches on its shell are evidence of this Pokémon’s toughness as a battler.",
        footer: "Tier 2 • [55-100%] • No. 8 / Base Set 1",
        img: "https://i.imgur.com/ynS9NVW.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/wartortle.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Bubble',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em>"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/water.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/fire.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/water.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/water.png">'
            }
        ]
    },
    12: {
        name: "Blastoise",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Blastoise has water spouts that protrude from its shell. The water spouts are very accurate. They can shoot bullets of water with enough accuracy to strike empty cans from a distance of over 160 feet.",
        footer: '',
        img: "https://i.imgur.com/uSrYEZE.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/blastoise.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    13: {
        name: "Mega Blastoise",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Blastoise has water spouts that protrude from its shell. The water spouts are very accurate. They can shoot bullets of water with enough accuracy to strike empty cans from a distance of over 160 feet.",
        footer: '',
        img: "https://i.imgur.com/7sLLBwx.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/blastoise-mega.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    181: {
        name: "Pidgey",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Pidgey has an extremely sharp sense of direction. It is capable of unerringly returning home to its nest, however far it may be removed from its familiar surroundings.",
        footer: "Tier 1 • [35-80%] • No. 16 / Base Set 1",
        img: "https://i.imgur.com/O5xYZAR.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pidgey.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  4   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  45   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Gust',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br><strong>5</strong>% Fixed Damage<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    182: {
        name: "Pidgeotto",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Pidgeotto claims a large area as its own territory. This Pokémon flies around, patrolling its living space. If its territory is violated, it shows no mercy in thoroughly punishing the foe with its sharp claws.",
        footer: "Tier 2 • [55-100%] • No. 17 / Base Set 1",
        img: "https://i.imgur.com/Kr1wfZy.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pidgeotto.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  63   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  60   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Wing Attack',
                value: "<strong>3</strong> PP 「<strong>AoE</strong>」<br><strong>10</strong>% Fixed Damage<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    41: {
        name: "Rattata",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Rattata is cautious in the extreme. Even while it is asleep, it constantly listens by moving its ears around. It is not picky about where it lives—it will make its nest anywhere.",
        footer: "Tier 1 • [35-80%] • No. 19 / Base Set 1",
        img: "https://i.imgur.com/yjfqBgm.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/rattata.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  30   <strong>PP</strong>:  4   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  56   <strong>Def</strong>:  35"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Tail Whip',
                value: "<strong>3</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    42: {
        name: "Raticate",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Raticate’s sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.",
        footer: "Tier 2 • [55-100%] • No. 20 / Base Set 1",
        img: "https://i.imgur.com/y22IYa6.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/raticate.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  81   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Rat Tail',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    43: {
        name: "Alolan Rattata",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Rattata is cautious in the extreme. Even while it is asleep, it constantly listens by moving its ears around. It is not picky about where it lives—it will make its nest anywhere.",
        footer: "Tier 2 • [55-100%] • No. 19 / Base Set 1",
        img: "https://i.imgur.com/d4TfePj.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/rattata-alola.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  30   <strong>PP</strong>:  4   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  56   <strong>Def</strong>:  35"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Tail Whip',
                value: "<strong>3</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    44: {
        name: "Alolan Raticate",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Raticate’s sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.",
        footer: "Tier 3 • [75-120%] • No. 20 / Base Set 1",
        img: "https://i.imgur.com/UuyTpVI.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/raticate-alola.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  81   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Rat Tail',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    15: {
        name: "Pichu",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "When Pichu plays with others, it may short out electricity with another Pichu, creating a shower of sparks. In that event, this Pokémon will begin crying, startled by the flash of sparks.",
        footer: "Tier 1 • [35-80%] • No. 172 / Base Set 1",
        img: "https://i.imgur.com/10Su2Te.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pichu.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  20   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  40   <strong>Def</strong>:  35"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Thunder Shock',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em><br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/electric.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/electric.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/electric.png">'
            }
        ]
    },
    16: {
        name: "Pikachu",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "This Pokémon has electricity-storing pouches on its cheeks. These appear to become electrically charged during the night while Pikachu sleeps. It occasionally discharges electricity when it is dozy after waking up.",
        footer: "Tier 2 • [55-100%] • No. 25 / Base Set 1",
        img: "https://i.imgur.com/gOzBcZP.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pikachu.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  35   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  55   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Thunderbolt',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em><br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/electric.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/electric.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/electric.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/electric.png">'
            }
        ]
    },
    17: {
        name: "Ash's Pikachu",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "This Pokémon has electricity-storing pouches on its cheeks. These appear to become electrically charged during the night while Pikachu sleeps. It occasionally discharges electricity when it is dozy after waking up.",
        footer: '',
        img: "https://i.imgur.com/vfJbVaT.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pikachu-original.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    60: {
        name: "Sandshrew",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Sandshrew has a very dry hide that is extremely tough. The Pokémon can roll into a ball that repels any attack. At night, it burrows into the desert sand to sleep.",
        footer: "Tier 2 • [55-100%] • No. 27 / Base Set 1",
        img: "https://i.imgur.com/6itqHhi.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/sandshrew.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  75   <strong>Def</strong>:  85"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sand Attack',
                value: '<strong>1</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.75</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More<br><img class="icon" src="images/types/earth.png">Earth Types in Party</em><br><br><strong>5</strong>% 🌪 Sandstorm<br>🎯 -<strong>1</strong> Enemy Accuracy'
            }
        ]
    },
    61: {
        name: "Sandslash",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Sandslash can roll up its body as if it were a ball covered with large spikes. In battle, this Pokémon will try to make the foe flinch by jabbing it with its spines. It then leaps at the stunned foe to tear wildly with its sharp claws.",
        footer: "Tier 3 • [75-120%] • No. 28 / Base Set 1",
        img: "https://i.imgur.com/arsebza.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/sandslash.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  75   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  100   <strong>Def</strong>:  110"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sandstorm',
                value: '<strong>1</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.75</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with More<br><img class="icon" src="images/types/earth.png">Earth Types in Party</em><br><br><strong>5</strong>% 🌪 Sandstorm<br>🎯 -<strong>1</strong> Enemy Accuracy'
            }
        ]
    },
    62: {
        name: "Alolan Sandshrew",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Sandshrew has a very dry hide that is extremely tough. The Pokémon can roll into a ball that repels any attack. At night, it burrows into the desert sand to sleep.",
        footer: "Tier 2 • [55-100%] • No. 27 / Base Set 1",
        img: "https://i.imgur.com/z8qJgym.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/sandshrew-alola.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  75   <strong>Def</strong>:  85"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Snow Attack',
                value: '<strong>1</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.75</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More<br><img class="icon" src="images/types/ice.png">Ice Types in Party</em><br><br><strong>5</strong>% ❄ Hail<br>🎯 -<strong>1</strong> Enemy Accuracy'
            }
        ]
    },
    63: {
        name: "Alolan Sandslash",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Sandslash can roll up its body as if it were a ball covered with large spikes. In battle, this Pokémon will try to make the foe flinch by jabbing it with its spines. It then leaps at the stunned foe to tear wildly with its sharp claws.",
        footer: "Tier 3 • [75-120%] • No. 28 / Base Set 1",
        img: "https://i.imgur.com/Xd3nSgp.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/sandslash-alola.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  75   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  100   <strong>Def</strong>:  110"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Snowstorm',
                value: '<strong>1</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.75</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with More<br><img class="icon" src="images/types/ice.png">Ice Types in Party</em><br><br><strong>5</strong>% ❄ Hail<br>🎯 -<strong>1</strong> Enemy Accuracy'
            }
        ]
    },
    194: {
        name: "Nidoran (Female)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Nidoran♀ has barbs that secrete a powerful poison. They are thought to have developed as protection for this small-bodied Pokémon. When enraged, it releases a horrible toxin from its horn.",
        footer: "Tier 1 • [35-80%] • No. 29 / Base Set 1",
        img: "https://i.imgur.com/qg96vy0.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/nidoranf.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  47   <strong>Def</strong>:  52"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Poison Pin',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with More Enemies</em><br><br><strong>15</strong>% 🍄 Poison Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    195: {
        name: "Nidorina",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "When Nidorina are with their friends or family, they keep their barbs tucked away to prevent hurting each other. This Pokémon appears to become nervous if separated from the others.",
        footer: "Tier 2 • [55-100%] • No. 30 / Base Set 1",
        img: "https://i.imgur.com/vFVowTs.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/nidorina.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  62   <strong>Def</strong>:  67"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Poison Horns',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More Enemies</em><br><br><strong>15</strong>% 🍄 Poison Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    197: {
        name: "Nidoran (Male)",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Nidoran♂ has developed muscles for moving its ears. Thanks to them, the ears can be freely moved in any direction. Even the slightest sound does not escape this Pokémon’s notice.",
        footer: "Tier 1 • [35-80%] • No. 32 / Base Set 1",
        img: "https://i.imgur.com/MsNpd71.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/nidoranm.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  46   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  57   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Poison Pin',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with More Enemies</em><br><br><strong>10</strong>% 🍄 Poison Infliction<br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    198: {
        name: "Nidorino",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Nidorino has a horn that is harder than a diamond. If it senses a hostile presence, all the barbs on its back bristle up at once, and it challenges the foe with all its might.",
        footer: "Tier 2 • [55-100%] • No. 33 / Base Set 1",
        img: "https://i.imgur.com/9GzkwPt.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/nidorino.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  61   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  72   <strong>Def</strong>:  57"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Poison Horns',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More Enemies</em><br><br><strong>10</strong>% 🍄 Poison Infliction<br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    26: {
        name: "Vulpix",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"> <strong>Burned</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Inside Vulpix’s body burns a flame that never goes out. During the daytime, when the temperatures rise, this Pokémon releases flames from its mouth to prevent its body from growing too hot.",
        footer: "Tier 2 • [55-100%] • No. 37 / Base Set 1",
        img: "https://i.imgur.com/nh04kYe.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/vulpix.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  38   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  50   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Cinder',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Strongest in Slot <strong>3</strong></em><br><br><strong>10</strong>% 🔥 Burn Infliction"
            }
        ]
    },
    27: {
        name: "Ninetales",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"> <strong>Burned</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Legend has it that Ninetales came into being when nine wizards possessing sacred powers merged into one. This Pokémon is highly intelligent—it can understand human speech.",
        footer: "Tier 3 • [75-120%] • No. 38 / Base Set 1",
        img: "https://i.imgur.com/Y3eoDu1.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/ninetales.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  73   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  81   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fire Spin',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Strongest in Slot <strong>3</strong></em><br><br><strong>15</strong>% 🔥 Burn Infliction"
            }
        ]
    },
    106: {
        name: "Alolan Vulpix",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Inside Vulpix’s body burns a flame that never goes out. During the daytime, when the temperatures rise, this Pokémon releases flames from its mouth to prevent its body from growing too hot. Its said to be extremely rare compared to its Firey counterpart, with some doubting its existence as nothing more than legend.",
        footer: "Tier 2 • [55-100%] • No. 37 / Base Set 1",
        img: "https://i.imgur.com/uV0qNKX.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/vulpix-alola.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  38   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  50   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fable',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Strongest in Slot <strong>3</strong></em><br><br><strong>10</strong>% 💥 Flinch Infliction<br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/rainbow.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/ice.png">+<strong>2</strong> PP<br><img class="icon" src="images/types/fairy.png">+<strong>2</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    107: {
        name: "Alolan Ninetales",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Legend has it that Ninetales came into being when nine wizards possessing sacred powers merged into one. This Pokémon is highly intelligent—it can understand human speech. Its said to be extremely rare compared to its Firey counterpart, with some doubting its existence as nothing more than legend.",
        footer: "Tier 3 • [75-120%] • No. 38 / Base Set 1",
        img: "https://i.imgur.com/MDIovQX.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/ninetales-alola.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  73   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  81   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Legend',
                value: "<strong>3</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Strongest in Slot <strong>3</strong></em><br><br><strong>10</strong>% 💥 Flinch Infliction<br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/rainbow.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/ice.png">+<strong>2</strong> PP<br><img class="icon" src="images/types/fairy.png">+<strong>2</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    92: {
        name: "Oddish",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Oddish searches for fertile, nutrient-rich soil, then plants itself. During the daytime, while it is planted, this Pokémon’s feet are thought to change shape and become similar to the roots of trees.",
        footer: "Tier 1 • [35-80%] • No. 43 / Base Set 1",
        img: "https://i.imgur.com/8BC4PRd.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/oddish.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  75   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Weed Spore',
                value: "<strong>1</strong> PP 「4 Random Targets」<br>Multi:  x<strong>0.8</strong> ~ <strong>1.1</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with More Enemies</em><br><br><strong>5</strong>% 🍄 Poison Infliction<br><strong>5</strong>% ⚡ Paralyze Infliction<br><strong>5</strong>% 💤 Sleep Infliction"
            }
        ]
    },
    93: {
        name: "Gloom",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "From its mouth Gloom drips honey that smells absolutely horrible. Apparently, it loves the horrid stench. It sniffs the noxious fumes and then drools even more of its honey.",
        footer: "Tier 2 • [55-100%] • No. 44 / Base Set 1",
        img: "https://i.imgur.com/QBQPAjs.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/gloom.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  85   <strong>Def</strong>:  75"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Petal Powder',
                value: "<strong>2</strong> PP 「4 Random Targets」<br>Multi:  x<strong>0.8</strong> ~ <strong>1.1</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More Enemies</em><br><br><strong>10</strong>% 🍄 Poison Infliction<br><strong>10</strong>% ⚡ Paralyze Infliction<br><strong>10</strong>% 💤 Sleep Infliction"
            }
        ]
    },
    94: {
        name: "Vileplume",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Vileplume has the world’s largest petals. They are used to attract prey that are then doused with toxic spores. Once the prey are immobilized, this Pokémon catches and devours them.",
        footer: '',
        img: "https://i.imgur.com/QiNtwRv.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/vileplume.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    45: {
        name: "Meowth",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Meowth withdraws its sharp claws into its paws to slinkily sneak about without making any incriminating footsteps. For some reason, this Pokémon loves shiny coins that glitter with light.",
        footer: "Tier 1 • [35-80%] • No. 52 / Base Set 1",
        img: "https://i.imgur.com/bbQgT8b.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/meowth.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  1   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  45   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Pay Day',
                value: "<strong>1</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]"
            }
        ]
    },
    46: {
        name: "Persian",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Persian has six bold whiskers that give it a look of toughness. The whiskers sense air movements to determine what is in the Pokémon’s surrounding vicinity. It becomes docile if grabbed by the whiskers.",
        footer: "Tier 2 • [55-100%] • No. 53 / Base Set 1",
        img: "https://i.imgur.com/oT0ruSS.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/persian.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  1   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> None',
                value: "<strong>1</strong> PP"
            }
        ]
    },
    47: {
        name: "Alolan Meowth",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Meowth withdraws its sharp claws into its paws to slinkily sneak about without making any incriminating footsteps. For some reason, this Pokémon loves shiny coins that glitter with light.",
        footer: "Tier 2 • [55-100%] • No. 52 / Base Set 1",
        img: "https://i.imgur.com/ixCocvE.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/meowth-alola.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  1   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  45   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Pay Day',
                value: "<strong>1</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]"
            }
        ]
    },
    48: {
        name: "Alolan Persian",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Persian has six bold whiskers that give it a look of toughness. The whiskers sense air movements to determine what is in the Pokémon’s surrounding vicinity. It becomes docile if grabbed by the whiskers.",
        footer: "Tier 3 • [75-120%] • No. 53 / Base Set 1",
        img: "https://i.imgur.com/kAIeHYq.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/persian-alola.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  1   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> None',
                value: "<strong>1</strong> PP"
            }
        ]
    },
    30: {
        name: "Growlithe",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Growlithe has a superb sense of smell. Once it smells anything, this Pokémon won’t forget the scent, no matter what. It uses its advanced olfactory sense to determine the emotions of other living things.",
        footer: "Tier 2 • [55-100%] • No. 58 / Base Set 1",
        img: "https://i.imgur.com/iQBSvIk.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/growlithe.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Bite',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>5</strong>% 🔥 Burn Infliction<br><strong>30</strong>% 💥 Flinch Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    110: {
        name: "Poliwag",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"> <strong>Confused</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Poliwag has a very thin skin. It is possible to see the Pokémon’s spiral innards right through the skin. Despite its thinness, however, the skin is also very flexible. Even sharp fangs bounce right off it.",
        footer: "Tier 1 • [35-80%] • No. 60 / Base Set 1",
        img: "https://i.imgur.com/2QjmUJF.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/poliwag.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  50   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Water Drop',
                value: "<strong>1</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><br><strong>10</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/water.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    111: {
        name: "Poliwhirl",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"> <strong>Confused</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "The surface of Poliwhirl’s body is always wet and slick with a slimy fluid. Because of this slippery covering, it can easily slip and slide out of the clutches of any enemy in battle.",
        footer: "Tier 2 • [55-100%] • No. 61 / Base Set 1",
        img: "https://i.imgur.com/SZSDjgZ.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/poliwhirl.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Whirlpool',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>10</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    80: {
        name: "Abra",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Abra needs to sleep for eighteen hours a day. If it doesn’t, this Pokémon loses its ability to use telekinetic powers. If it is attacked, Abra escapes using Teleport while it is still sleeping.",
        footer: "Tier 1 • [35-80%] • No. 63 / Base Set 1",
        img: "https://i.imgur.com/5lM1FEy.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/abra.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  25   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  105   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Psywave',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em><br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/earth.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/psychic.png">'
            }
        ]
    },
    81: {
        name: "Kadabra",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Kadabra holds a silver spoon in its hand. The spoon is used to amplify the alpha waves in its brain. Without the spoon, the Pokémon is said to be limited to half the usual amount of its telekinetic powers.",
        footer: "Tier 2 • [55-100%] • No. 64 / Base Set 1",
        img: "https://i.imgur.com/qQ2h1us.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/kadabra.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  120   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Kinesis',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em><br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/earth.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/psychic.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/psychic.png">'
            }
        ]
    },
    82: {
        name: "Alakazam",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Alakazam’s brain continually grows, infinitely multiplying brain cells. This amazing brain gives this Pokémon an astoundingly high IQ of 5,000. It has a thorough memory of everything that has occurred in the world.",
        footer: '',
        img: "https://i.imgur.com/A9aqdRd.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/alakazam.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    108: {
        name: "Magnemite",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Magnemite floats in the air by emitting electromagnetic waves from the units at its sides. These waves block gravity. This Pokémon becomes incapable of flight if its internal electrical supply is depleted.",
        footer: "Tier 1 • [35-80%] • No. 81 / Base Set 1",
        img: "https://i.imgur.com/ljW6mYU.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/magnemite.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  25   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  95   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Magnetize',
                value: '<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.8</strong> ~ <strong>1.2</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with More<br><img class="icon" src="images/types/electric.png">Electric Types in Party</em><br><br><strong>5</strong>% ⚡ Paralyze Infliction'
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/normal.png"> Def +<strong>1</strong>'
            }
        ]
    },
    109: {
        name: "Magneton",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Magneton emits a powerful magnetic force that is fatal to electronics and precision instruments. Because of this, it is said that some towns warn people to keep this Pokémon inside a Poké Ball.",
        footer: "Tier 2 • [55-100%] • No. 82 / Base Set 1",
        img: "https://i.imgur.com/bqtXmLB.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/magneton.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  120   <strong>Def</strong>:  95"
            },
            {
                name: '<img class="icon" src="images/sword.png"> E.M.P.',
                value: '<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.8</strong> ~ <strong>1.2</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More<br><img class="icon" src="images/types/electric.png">Electric Types in Party</em><br><br><strong>5</strong>% ⚡ Paralyze Infliction'
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '2 Turn: <img class="icon" src="images/types/normal.png"> Def +<strong>1</strong>'
            }
        ]
    },
    69: {
        name: "Gastly",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"> <strong>Sleeping</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Gastly is largely composed of gaseous matter. When exposed to a strong wind, the gaseous body quickly dwindles away. Groups of this Pokémon cluster under the eaves of houses to escape the ravages of wind.",
        footer: "Tier 1 • [35-80%] • No. 92 / Base Set 1",
        img: "https://i.imgur.com/QRVhpFO.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/gastly.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  30   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  100   <strong>Def</strong>:  35"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Haunt',
                value: "<strong>1</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Fewer Enemies</em><br><strong>Recoil!</strong> Lose all but <strong>1</strong> HP<br><br><strong>5</strong>% 💤 Sleep Infliction<br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    70: {
        name: "Haunter",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"> <strong>Sleeping</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Haunter is a dangerous Pokémon. If one beckons you while floating in darkness, you must never approach it. This Pokémon will try to lick you with its tongue and steal your life away.",
        footer: "Tier 2 • [55-100%] • No. 93 / Base Set 1",
        img: "https://i.imgur.com/TPYJTeg.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/haunter.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  115   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Dream Eater',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Fewer Enemies</em><br><strong>Recoil!</strong> Lose all but <strong>1</strong> HP<br><br><strong>10</strong>% 💤 Sleep Infliction<br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    71: {
        name: "Gengar",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"> <strong>Sleeping</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Sometimes, on a dark night, your shadow thrown by a streetlight will suddenly and startlingly overtake you. It is actually a Gengar running past you, pretending to be your shadow.",
        footer: '',
        img: "https://i.imgur.com/9wWw0cC.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/gengar.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    83: {
        name: "Onix",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Onix has a magnet in its brain. It acts as a compass so that this Pokémon does not lose direction while it is tunneling. As it grows older, its body becomes increasingly rounder and smoother.",
        footer: "Tier 1 • [35-80%] • No. 95 / Base Set 1",
        img: "https://i.imgur.com/nJ5WtXw.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/onix.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  35   <strong>PP</strong>:  6   <strong>Wt</strong>: Heavy<br><strong>Atk</strong>:  45   <strong>Def</strong>:  160"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Bind',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em><br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/earth.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/electric.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/earth.png">'
            }
        ]
    },
    84: {
        name: "Brock's Onix",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Onix has a magnet in its brain. It acts as a compass so that this Pokémon does not lose direction while it is tunneling. As it grows older, its body becomes increasingly rounder and smoother.",
        footer: "Tier 2 • [55-100%] • No. 95 / Base Set 1",
        img: "https://i.imgur.com/K9aYwcQ.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/onix.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  35   <strong>PP</strong>:  6   <strong>Wt</strong>: Heavy<br><strong>Atk</strong>:  45   <strong>Def</strong>:  160"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Bind',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em><br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/earth.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/electric.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/earth.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/earth.png">'
            }
        ]
    },
    85: {
        name: "Steelix",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Steelix lives even further underground than Onix. This Pokémon is known to dig toward the earth’s core. There are records of this Pokémon reaching a depth of over six-tenths of a mile underground.",
        footer: '',
        img: "https://i.imgur.com/fi2MsHS.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/steelix.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Titan<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    228: {
        name: "Mega Steelix",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Steelix lives even further underground than Onix. This Pokémon is known to dig toward the earth’s core. There are records of this Pokémon reaching a depth of over six-tenths of a mile underground.",
        footer: '',
        img: "https://i.imgur.com/xVVf4q8.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/steelix-mega.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Titan<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    209: {
        name: "Voltorb",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Voltorb is extremely sensitive—it explodes at the slightest of shocks. It is rumored that it was first created when a Poké Ball was exposed to a powerful pulse of energy.",
        footer: "Tier 2 • [55-100%] • No. 100 / Base Set 1",
        img: "https://i.imgur.com/vmIXOMM.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/voltorb.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  55   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Self-Destruct',
                value: "<strong>5</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>2.5</strong> ~ <strong>3.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Higher HP</em><br>💣 Faint after damage<br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            }
        ]
    },
    210: {
        name: "Electrode",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "One of Electrode’s characteristics is its attraction to electricity. It is a problematical Pokémon that congregates mostly at electrical power plants to feed on electricity that has just been generated.",
        footer: "Tier 3 • [75-120%] • No. 101 / Base Set 1",
        img: "https://i.imgur.com/gg0DKhz.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/electrode.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Self-Destruct+',
                value: "<strong>5</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>2.5</strong> ~ <strong>3.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Higher HP</em><br>💣 Faint after damage<br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            }
        ]
    },
    64: {
        name: "Happiny",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "It carefully carries a round, white rock that it thinks is an egg. It’s bothered by how curly its hair looks.",
        footer: "Tier 1 • [35-80%] • No. 440 / Base Set 1",
        img: "https://i.imgur.com/UL9iBP3.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/happiny.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  100   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  15   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Petit Egg',
                value: "<strong>1</strong> PP"
            },
            {
                name: "❤ Heal",
                value: "Restores <strong>2/3</strong> of Party HP<br><em>Cures all status ailments</em>"
            }
        ]
    },
    65: {
        name: "Chansey",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Chansey lays nutritionally excellent eggs on an everyday basis. The eggs are so delicious, they are easily and eagerly devoured by even those people who have lost their appetite.",
        footer: "Tier 2 • [55-100%] • No. 113 / Base Set 1",
        img: "https://i.imgur.com/FRVOTFR.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/chansey.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  250   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  35   <strong>Def</strong>:  105"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Soft-Boiled',
                value: "<strong>2</strong> PP"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Atk +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/rainbow.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            },
            {
                name: "❤ Heal",
                value: "Restores <strong>2/3</strong> of Party HP<br><em>Cures all status ailments</em>"
            }
        ]
    },
    66: {
        name: "Blissey",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Blissey senses sadness with its fluffy coat of fur. If it does so, this Pokémon will rush over to a sad person, no matter how far away, to share a Lucky Egg that brings a smile to any face.",
        footer: '',
        img: "https://i.imgur.com/N18Rs8r.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/blissey.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    54: {
        name: "Mime Jr. (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "It habitually mimics foes. Once mimicked, the foe cannot take its eyes off this Pokémon.",
        footer: "Tier 2 • [55-100%] • No. 439 / Base Set 1",
        img: "https://i.imgur.com/IuMFqSg.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/mimejr.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  20   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  90"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Mini Barrier',
                value: "<strong>1</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: "Reflect +<strong>1</strong>"
            }
        ]
    },
    55: {
        name: "Mr. Mime (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Mr. Mime is a master of pantomime. Its gestures and motions convince watchers that something unseeable actually exists. Once the watchers are convinced, the unseeable thing exists as if it were real.",
        footer: "Tier 3 • [75-120%] • No. 122 / Base Set 1",
        img: "https://i.imgur.com/MH7f5zE.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/mrmime.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  100   <strong>Def</strong>:  120"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Barrier',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: "Reflect +<strong>2</strong>"
            }
        ]
    },
    56: {
        name: "Mime Jr. (Fairy)",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "It habitually mimics foes. Once mimicked, the foe cannot take its eyes off this Pokémon.",
        footer: "Tier 2 • [55-100%] • No. 439 / Base Set 1",
        img: "https://i.imgur.com/JkYL7m7.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/mimejr.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  20   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  90"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Mini Barrier',
                value: "<strong>1</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: "Reflect +<strong>1</strong>"
            }
        ]
    },
    57: {
        name: "Mr. Mime (Fairy)",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "Mr. Mime is a master of pantomime. Its gestures and motions convince watchers that something unseeable actually exists. Once the watchers are convinced, the unseeable thing exists as if it were real.",
        footer: "Tier 3 • [75-120%] • No. 122 / Base Set 1",
        img: "https://i.imgur.com/TTnJEVw.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/mrmime.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  100   <strong>Def</strong>:  120"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Barrier',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: "Reflect +<strong>2</strong>"
            }
        ]
    },
    190: {
        name: "Scyther",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Scyther is blindingly fast. Its blazing speed enhances the effectiveness of the twin scythes on its forearms. This Pokémon’s scythes are so effective, they can slice through thick logs in one wicked stroke.",
        footer: "Tier 3 • [75-120%] • No. 123 / Base Set 1",
        img: "https://i.imgur.com/wzA1YOr.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/scyther.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  110   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Hyper Scythe',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Later Slot</em><br><strong>Recoil!</strong> Lose <strong>10</strong>% of max HP<br>⏱ Recharge: <strong>1</strong> Turn"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"> Atk +<strong>2</strong>'
            }
        ]
    },
    191: {
        name: "Scizor",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Scizor has a body with the hardness of steel. It is not easily fazed by ordinary sorts of attacks. This Pokémon flaps its wings to regulate its body temperature.",
        footer: "Tier 3 • [75-120%] • No. 212 / Base Set 1",
        img: "https://i.imgur.com/1xzROZy.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/scizor.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Mid<br><strong>Atk</strong>:  130   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Hyper Steel',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Later Slot</em><br><strong>Recoil!</strong> Lose <strong>10</strong>% of max HP<br>⏱ Recharge: <strong>1</strong> Turn<br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"> Atk +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '2 Turn: <img class="icon" src="images/types/normal.png"> Def +<strong>1</strong>'
            }
        ]
    },
    170: {
        name: "Smoochum",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Smoochum actively runs about, but also falls quite often. Whenever the chance arrives, it will look for its reflection to make sure its face hasn’t become dirty.",
        footer: "Tier 2 • [55-100%] • No. 238 / Base Set 1",
        img: "https://i.imgur.com/oiotmyn.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/smoochum.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  85   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Smooch',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>20</strong>% 💕 Charm Infliction<br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/ice.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    171: {
        name: "Jynx",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Jynx walks rhythmically, swaying and shaking its hips as if it were dancing. Its motions are so bouncingly alluring, people seeing it are compelled to shake their hips without giving any thought to what they are doing.",
        footer: "Tier 3 • [75-120%] • No. 124 / Base Set 1",
        img: "https://i.imgur.com/m87FPUQ.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/jynx.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  115   <strong>Def</strong>:  95"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Heart of Ice',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>20</strong>% 💕 Charm Infliction<br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/ice.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    86: {
        name: "Elekid",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Elekid stores electricity in its body. If it touches metal and accidentally discharges all its built-up electricity, this Pokémon begins swinging its arms in circles to recharge itself.",
        footer: "Tier 2 • [55-100%] • No. 239 / Base Set 1",
        img: "https://i.imgur.com/9OXLlz2.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/elekid.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Thunder Ball',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>10</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/electric.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    87: {
        name: "Electabuzz",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "When a storm arrives, gangs of this Pokémon compete with each other to scale heights that are likely to be stricken by lightning bolts. Some towns use Electabuzz in place of lightning rods.",
        footer: "Tier 3 • [75-120%] • No. 125 / Base Set 1",
        img: "https://i.imgur.com/WNq456y.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/electabuzz.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  95   <strong>Def</strong>:  85"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Thunder Punch',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>10</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/electric.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    28: {
        name: "Magby",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Magby’s state of health is determined by observing the fire it breathes. If the Pokémon is spouting yellow flames from its mouth, it is in good health. When it is fatigued, black smoke will be mixed in with the flames.",
        footer: "Tier 2 • [55-100%] • No. 240 / Base Set 1",
        img: "https://i.imgur.com/WF53MvH.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/magby.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  75   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Lava Bubble',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>10</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    29: {
        name: "Magmar",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "In battle, Magmar blows out intensely hot flames from all over its body to intimidate its opponent. This Pokémon’s fiery bursts create heat waves that ignite grass and trees in its surroundings.",
        footer: "Tier 3 • [75-120%] • No. 126 / Base Set 1",
        img: "https://i.imgur.com/wtVYfqK.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/magmar.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  100   <strong>Def</strong>:  85"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Lava Burst',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>10</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    58: {
        name: "Magikarp",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Magikarp is virtually useless in battle as it can only splash around. As a result, it is considered to be weak. However, it is actually a very hardy Pokémon that can survive in any body of water no matter how polluted it is.",
        footer: "Tier 1 • [35-80%] • No. 129 / Base Set 1",
        img: "https://i.imgur.com/CYHfx7j.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/magikarp.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  20   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  15   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Splash',
                value: "<strong>1</strong> PP"
            }
        ]
    },
    59: {
        name: "Gyarados (Dragon)",
        desc: '<img class="icon" src="images/types/dragon.png">Dragon Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png">',
        bio: "Once Gyarados goes on a rampage, its ferociously violent blood doesn’t calm until it has burned everything down. There are records of this Pokémon’s rampages lasting a whole month.",
        footer: "Tier 3 • [75-120%] • No. 130 / Base Set 1",
        img: "https://i.imgur.com/EGNJODe.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/gyarados.gif",
        type: 10,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  95   <strong>PP</strong>:  4   <strong>Wt</strong>: Heavy<br><strong>Atk</strong>:  125   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Dragon Rage',
                value: "<strong>4</strong> PP 「Single Target」<br><strong>50</strong>% Fixed Damage<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><strong>Recoil!</strong> Lose <strong>50</strong>% of max HP"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong><br><img class="icon" src="images/types/dragon.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    79: {
        name: "Ditto",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Ditto rearranges its cell structure to transform itself into other shapes. However, if it tries to transform itself into something by relying on its memory, this Pokémon manages to get details wrong.",
        footer: "Tier 2 • [55-100%] • No. 132 / Base Set 1",
        img: "https://i.imgur.com/1Fisxc3.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/ditto.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  48   <strong>PP</strong>:  2   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  48   <strong>Def</strong>:  48"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Transform',
                value: "<strong>2</strong> PP<br>Copies the Pokémon after this one."
            }
        ]
    },
    37: {
        name: "Eevee",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Eevee has an unstable genetic makeup that suddenly mutates due to the environment in which it lives. Radiation from various stones causes this Pokémon to evolve.",
        footer: "Tier 2 • [55-100%] • No. 133 / Base Set 1",
        img: "https://i.imgur.com/iH2uonR.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/eevee.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  55   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Tackle',
                value: "<strong>1</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]"
            }
        ]
    },
    38: {
        name: "Vaporeon",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Vaporeon underwent a spontaneous mutation and grew fins and gills that allow it to live underwater. This Pokémon has the ability to freely control water.",
        footer: "Tier 3 • [75-120%] • No. 134 / Base Set 1",
        img: "https://i.imgur.com/bcoYTgz.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/vaporeon.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  130   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  110   <strong>Def</strong>:  95"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Bubble Jet',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><strong>Recoil!</strong> Lose <strong>20</strong>% of max HP"
            },
            {
                name: '<span class="icon-num">1</span> Attack Buff',
                value: '<img class="icon" src="images/types/water.png"> Enemy Def -<strong>3</strong>'
            }
        ]
    },
    39: {
        name: "Jolteon",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "They send out electrical charges of about 10,000 volts. Because they are high-strung, it can be difficult to grow close to them.",
        footer: "Tier 3 • [75-120%] • No. 135 / Base Set 1",
        img: "https://i.imgur.com/k8rfOK8.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/jolteon.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  110   <strong>Def</strong>:  95"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Spark',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><strong>Recoil!</strong> Lose <strong>20</strong>% of max HP<br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Attack Buff',
                value: '<img class="icon" src="images/types/electric.png"> Enemy Def -<strong>3</strong>'
            }
        ]
    },
    40: {
        name: "Flareon",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Flareon’s fluffy fur has a functional purpose—it releases heat into the air so that its body does not get excessively hot. This Pokémon’s body temperature can rise to a maximum of 1,650 degrees Fahrenheit.",
        footer: "Tier 3 • [75-120%] • No. 136 / Base Set 1",
        img: "https://i.imgur.com/8qQS8BA.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/flareon.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  130   <strong>Def</strong>:  110"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Flare',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><strong>Recoil!</strong> Lose <strong>20</strong>% of max HP<br><br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Attack Buff',
                value: '<img class="icon" src="images/types/fire.png"> Enemy Def -<strong>3</strong>'
            }
        ]
    },
    74: {
        name: "Porygon",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Porygon is capable of reverting itself entirely back to program data and entering cyberspace. This Pokémon is copy protected so it cannot be duplicated by copying.",
        footer: "Tier 2 • [55-100%] • No. 137 / Base Set 1",
        img: "https://i.imgur.com/UuzQKIr.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/porygon.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  85   <strong>Def</strong>:  75"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Conversion',
                value: "<strong>2</strong> PP<br>Copies the Pokémon before this one."
            }
        ]
    },
    75: {
        name: "Porygon2",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Porygon2 was created by humans using the power of science. The man-made Pokémon has been endowed with artificial intelligence that enables it to learn new gestures and emotions on its own.",
        footer: '',
        img: "https://i.imgur.com/h1CgUgb.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/porygon2.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    76: {
        name: "Porygon-Z",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Its programming was modified to enable it to travel through alien dimensions. Seems there might have been an error...",
        footer: '',
        img: "https://i.imgur.com/vnRWa8h.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/porygon-z.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  ?   <strong>PP</strong>:  ?   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  ?   <strong>Def</strong>:  ?"
            },
            {
                name: '<img class="icon" src="images/sword.png"> ???',
                value: "???"
            }
        ]
    },
    67: {
        name: "Munchlax",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "It conceals food under the long fur on its body. It carts around this food stash and swallows it without chewing.",
        footer: "Tier 1 • [35-80%] • No. 446 / Base Set 1",
        img: "https://i.imgur.com/tx2OHsd.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/munchlax.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  135   <strong>PP</strong>:  5   <strong>Wt</strong>: Mid<br><strong>Atk</strong>:  85   <strong>Def</strong>:  85"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Nap',
                value: "<strong>2</strong> PP<br>Puts your party to sleep 💤"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: "💤 Sleep Talk<br><em>Can attack while sleeping.</em>"
            },
            { name: "❤ Heal", value: "Restores <strong>all</strong> Party HP" }
        ]
    },
    68: {
        name: "Snorlax",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Snorlax’s typical day consists of nothing more than eating and sleeping. It is such a docile Pokémon that there are children who use its expansive belly as a place to play.",
        footer: "Tier 3 • [75-120%] • No. 143 / Base Set 1",
        img: "https://i.imgur.com/8wzltIk.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/snorlax.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  160   <strong>PP</strong>:  9   <strong>Wt</strong>: Titan<br><strong>Atk</strong>:  110   <strong>Def</strong>:  110"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Rest',
                value: "<strong>3</strong> PP<br>Puts your party to sleep 💤"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: "💤 Sleep Talk<br><em>Can attack while sleeping.</em>"
            },
            {
                name: "❤ Heal",
                value: "Restores <strong>all</strong> Party HP<br><em>Cures all status ailments</em>"
            }
        ]
    },
    167: {
        name: "Hoothoot",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type<br><em>Strong Against:</em>  <strong>Sleeping</strong> Pokémon',
        bio: "Hoothoot has an internal organ that senses and tracks the earth’s rotation. Using this special organ, this Pokémon begins hooting at precisely the same time every day.",
        footer: "Tier 1 • [35-80%] • No. 163 / Base Set 1",
        img: "https://i.imgur.com/tuM5IYW.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/hoothoot.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  36   <strong>Def</strong>:  56"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Insomnia',
                value: '<strong>1</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.68</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with More<br><img class="icon" src="images/types/dark.png">Dark Types in Party</em><br><br><strong>10</strong>% 💤 Sleep Infliction'
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>8</strong>% Z-Move for all<img class="icon" src="images/types/dark.png">'
            }
        ]
    },
    168: {
        name: "Noctowl",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type<br><em>Strong Against:</em>  <strong>Sleeping</strong> Pokémon',
        bio: "Noctowl never fails at catching prey in darkness. This Pokémon owes its success to its superior vision that allows it to see in minimal light, and to its soft, supple wings that make no sound in flight.",
        footer: "Tier 2 • [55-100%] • No. 164 / Base Set 1",
        img: "https://i.imgur.com/Sh9oJc6.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/noctowl.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  100   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  76   <strong>Def</strong>:  96"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Midnight Hunt',
                value: '<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.68</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More<br><img class="icon" src="images/types/dark.png">Dark Types in Party</em><br><br><strong>10</strong>% 💤 Sleep Infliction'
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>8</strong>% Z-Move for all<img class="icon" src="images/types/dark.png">'
            }
        ]
    },
    123: {
        name: "Togepi",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "As its energy, Togepi uses the positive emotions of compassion and pleasure exuded by people and Pokémon. This Pokémon stores up feelings of happiness inside its shell, then shares them with others.",
        footer: "Tier 1 • [35-80%] • No. 175 / Base Set 1",
        img: "https://i.imgur.com/Yr5RrXw.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/togepi.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  35   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  40   <strong>Def</strong>:  65"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Charm',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em><br><br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/dark.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/fairy.png">'
            }
        ]
    },
    124: {
        name: "Togetic",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "Togetic is said to be a Pokémon that brings good fortune. When the Pokémon spots someone who is pure of heart, it is said to appear and share its happiness with that person.",
        footer: "Tier 2 • [55-100%] • No. 176 / Base Set 1",
        img: "https://i.imgur.com/J6eDcxs.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/togetic.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  80   <strong>Def</strong>:  105"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fairy Wind',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em><br><br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/dark.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/fairy.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/fairy.png">'
            }
        ]
    },
    114: {
        name: "Mareep",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"> <strong>Paralyzed</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Mareep’s fluffy coat of wool rubs together and builds a static charge. The more static electricity is charged, the more brightly the lightbulb at the tip of its tail glows.",
        footer: "Tier 1 • [35-80%] • No. 179 / Base Set 1",
        img: "https://i.imgur.com/orbr9ZV.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/mareep.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  45"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Cotton Static',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Strongest in Slot <strong>3</strong></em><br><br><strong>10</strong>% ⚡ Paralyze Infliction"
            }
        ]
    },
    115: {
        name: "Flaaffy",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"> <strong>Paralyzed</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Flaaffy’s wool quality changes so that it can generate a high amount of static electricity with a small amount of wool. The bare and slick parts of its hide are shielded against electricity.",
        footer: "Tier 2 • [55-100%] • No. 180 / Base Set 1",
        img: "https://i.imgur.com/uqA6obq.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/flaaffy.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Static Shock',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Strongest in Slot <strong>3</strong></em><br><br><strong>10</strong>% ⚡ Paralyze Infliction"
            }
        ]
    },
    112: {
        name: "Azurill",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Azurill’s tail is large and bouncy. It is packed full of the nutrients this Pokémon needs to grow. Azurill can be seen bouncing and playing on its big, rubbery tail.",
        footer: "Tier 1 • [35-80%] • No. 298 / Base Set 1",
        img: "https://i.imgur.com/8Ajnhrg.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/azurill.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  4   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  20   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fairy Splash',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"> Def +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/water.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    113: {
        name: "Marill",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "When fishing for food at the edge of a fast-running stream, Marill wraps its tail around the trunk of a tree. This Pokémon’s tail is flexible and configured to stretch.",
        footer: "Tier 2 • [55-100%] • No. 183 / Base Set 1",
        img: "https://i.imgur.com/LPiqMfk.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/marill.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  20   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fairy Bubble',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"> Def +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/water.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    119: {
        name: "Murkrow",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Murkrow was feared and loathed as the alleged bearer of ill fortune. This Pokémon shows strong interest in anything that sparkles or glitters. It will even try to steal rings from women.",
        footer: "Tier 2 • [55-100%] • No. 198 / Base Set 1",
        img: "https://i.imgur.com/cpScHZU.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/murkrow.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  4   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  85   <strong>Def</strong>:  42"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Black Feather',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/dark.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/dark.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    105: {
        name: "Unown",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "This Pokémon is shaped like ancient writing. It is a mystery as to which came first, the ancient writings or the various Unown. Research into this topic is ongoing but nothing is known. Its power is said to be one of the most mysterious.",
        footer: "Tier 2 • [55-100%] • No. 201 / Base Set 1",
        img: "https://i.imgur.com/uhaJp3X.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/unown-f.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  48   <strong>PP</strong>:  8   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  72   <strong>Def</strong>:  48"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Hidden Power',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.8</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Lower HP</em><br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: "+<strong>40</strong>% Z-Move for all Pokémon starting with its letter"
            }
        ]
    },
    205: {
        name: "Snubbull",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "By baring its fangs and making a scary face, Snubbull sends smaller Pokémon scurrying away in terror. However, this Pokémon seems a little sad at making its foes flee.",
        footer: "Tier 2 • [55-100%] • No. 209 / Base Set 1",
        img: "https://i.imgur.com/VMx9q9Q.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/snubbull.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Play Rough',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>10</strong>% 💥 Flinch Infliction<br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/fairy.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    206: {
        name: "Granbull",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "Granbull has a particularly well-developed lower jaw. The enormous fangs are heavy, causing the Pokémon to tip its head back for balance. Unless it is startled, it will not try to bite indiscriminately.",
        footer: "Tier 3 • [75-120%] • No. 210 / Base Set 1",
        img: "https://i.imgur.com/6Oz0JBP.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/granbull.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  90   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  120   <strong>Def</strong>:  75"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Crushing Jaw',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>10</strong>% 💥 Flinch Infliction<br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/fairy.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    162: {
        name: "Sneasel (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Sneasel scales trees by punching its hooked claws into the bark. This Pokémon seeks out unguarded nests and steals eggs for food while the parents are away.",
        footer: "Tier 2 • [55-100%] • No. 215 / Base Set 1",
        img: "https://i.imgur.com/jks6llK.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/sneasel.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  95   <strong>Def</strong>:  75"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Icey Swipe',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>5</strong>% 💥 Flinch Infliction<br>🎯 -<strong>1</strong> Enemy Accuracy"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/ice.png"><img class="icon" src="images/types/dark.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    163: {
        name: "Weavile (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "They live in cold regions, forming groups of four or five that hunt prey with impressive coordination.",
        footer: "Tier 3 • [75-120%] • No. 461 / Base Set 1",
        img: "https://i.imgur.com/Kz7cVBU.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/weavile.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  120   <strong>Def</strong>:  85"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Ice Scythe',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>5</strong>% 💥 Flinch Infliction<br>🎯 -<strong>1</strong> Enemy Accuracy"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/ice.png"><img class="icon" src="images/types/dark.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    164: {
        name: "Sneasel (Ice)",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Sneasel scales trees by punching its hooked claws into the bark. This Pokémon seeks out unguarded nests and steals eggs for food while the parents are away.",
        footer: "Tier 2 • [55-100%] • No. 215 / Base Set 1",
        img: "https://i.imgur.com/Kmrj2Fy.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/sneasel.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  95   <strong>Def</strong>:  75"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Icey Swipe',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>5</strong>% 💥 Flinch Infliction<br><strong>5</strong>% ❄ Hail<br>🎯 -<strong>1</strong> Enemy Accuracy"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/ice.png"><img class="icon" src="images/types/dark.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    165: {
        name: "Weavile (Ice)",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "They live in cold regions, forming groups of four or five that hunt prey with impressive coordination.",
        footer: "Tier 3 • [75-120%] • No. 461 / Base Set 1",
        img: "https://i.imgur.com/bjx7hyY.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/weavile.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  120   <strong>Def</strong>:  85"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Ice Scythe',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>5</strong>% 💥 Flinch Infliction<br><strong>5</strong>% ❄ Hail<br>🎯 -<strong>1</strong> Enemy Accuracy"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/ice.png"><img class="icon" src="images/types/dark.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    192: {
        name: "Teddiursa",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "This Pokémon likes to lick its palms that are sweetened by being soaked in honey. Teddiursa concocts its own honey by blending fruits and pollen collected by Beedrill.",
        footer: "Tier 2 • [55-100%] • No. 216 / Base Set 1",
        img: "https://i.imgur.com/17sKRIO.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/teddiursa.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Small Roar',
                value: "<strong>1</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>3</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/rainbow.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    193: {
        name: "Ursaring",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "In the forests inhabited by Ursaring, it is said that there are many streams and towering trees where they gather food. This Pokémon walks through its forest gathering food every day.",
        footer: "Tier 3 • [75-120%] • No. 217 / Base Set 1",
        img: "https://i.imgur.com/avQefTf.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/ursaring.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  90   <strong>PP</strong>:  8   <strong>Wt</strong>: Mid<br><strong>Atk</strong>:  130   <strong>Def</strong>:  75"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Roar',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/rainbow.png"> Atk +<strong>3</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/rainbow.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    20: {
        name: "Houndour (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Houndour hunt as a coordinated pack. They communicate with each other using a variety of cries to corner their prey. This Pokémon’s remarkable teamwork is unparalleled.",
        footer: "Tier 2 • [55-100%] • No. 228 / Base Set 1",
        img: "https://i.imgur.com/oF36E58.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/houndour.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Crunch',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Strongest in Slot <strong>4</strong></em>"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    21: {
        name: "Houndoom (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "In a Houndoom pack, the one with its horns raked sharply toward the back serves a leadership role. These Pokémon choose their leader by fighting among themselves.",
        footer: "Tier 3 • [75-120%] • No. 229 / Base Set 1",
        img: "https://i.imgur.com/bHnBskv.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/houndoom.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  75   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  110   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fire Fang',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Strongest in Slot <strong>4</strong></em>"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    23: {
        name: "Houndour (Fire)",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Houndour hunt as a coordinated pack. They communicate with each other using a variety of cries to corner their prey. This Pokémon’s remarkable teamwork is unparalleled.",
        footer: "Tier 2 • [55-100%] • No. 228 / Base Set 1",
        img: "https://i.imgur.com/LWfnKke.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/houndour.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Crunch',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Strongest in Slot <strong>4</strong></em><br><br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    24: {
        name: "Houndoom (Fire)",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "In a Houndoom pack, the one with its horns raked sharply toward the back serves a leadership role. These Pokémon choose their leader by fighting among themselves.",
        footer: "Tier 3 • [75-120%] • No. 229 / Base Set 1",
        img: "https://i.imgur.com/YVDRWSF.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/houndoom.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  75   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  110   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fire Fang',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Strongest in Slot <strong>4</strong></em><br><br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    223: {
        name: "Miltank",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Miltank gives over five gallons of milk on a daily basis. Its sweet milk is enjoyed by children and grown-ups alike. People who can’t drink milk turn it into yogurt and eat it instead.",
        footer: "Tier 2 • [55-100%] • No. 241 / Base Set 1",
        img: "https://i.imgur.com/DeiBt7i.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/miltank.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  95   <strong>PP</strong>:  8   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  105"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Rollout',
                value: "<strong>2</strong> PP 「1 Random Target」<br>Multi:  x<strong>0.5</strong> ~ <strong>8.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Each Turn</em>"
            }
        ]
    },
    129: {
        name: "Larvitar (Earth)",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Larvitar is born deep under the ground. To come up to the surface, this Pokémon must eat its way through the soil above. Until it does so, Larvitar cannot see its parents.",
        footer: "Tier 1 • [35-80%] • No. 246 / Base Set 1",
        img: "https://i.imgur.com/Qrd7m4T.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/larvitar.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  64   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Toss',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Stronger against heavy foes</em><br><br><strong>5</strong>% 💫 Confusion Infliction<br><strong>5</strong>% 🌪 Sandstorm<br>🎯 -<strong>1</strong> Enemy Accuracy"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    133: {
        name: "Larvitar (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Larvitar is born deep under the ground. To come up to the surface, this Pokémon must eat its way through the soil above. Until it does so, Larvitar cannot see its parents.",
        footer: "Tier 1 • [35-80%] • No. 246 / Base Set 1",
        img: "https://i.imgur.com/uVTtAWS.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/larvitar.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  64   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Toss',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Stronger against heavy foes</em><br><br><strong>5</strong>% 💫 Confusion Infliction<br>🎯 -<strong>1</strong> Enemy Accuracy"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    130: {
        name: "Pupitar (Earth)",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Pupitar creates a gas inside its body that it compresses and forcefully ejects to propel itself like a jet. The body is very durable—it avoids damage even if it hits solid steel.",
        footer: "Tier 2 • [55-100%] • No. 247 / Base Set 1",
        img: "https://i.imgur.com/7dwBTcO.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pupitar.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Mid<br><strong>Atk</strong>:  84   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Stone Bash',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Stronger against heavy foes</em><br><br><strong>5</strong>% 💫 Confusion Infliction<br><strong>5</strong>% 🌪 Sandstorm<br>🎯 -<strong>1</strong> Enemy Accuracy"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    134: {
        name: "Pupitar (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Pupitar creates a gas inside its body that it compresses and forcefully ejects to propel itself like a jet. The body is very durable—it avoids damage even if it hits solid steel.",
        footer: "Tier 2 • [55-100%] • No. 247 / Base Set 1",
        img: "https://i.imgur.com/OewEBLE.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pupitar.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Mid<br><strong>Atk</strong>:  84   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Stone Bash',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Stronger against heavy foes</em><br><br><strong>5</strong>% 💫 Confusion Infliction<br>🎯 -<strong>1</strong> Enemy Accuracy"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    137: {
        name: "Lotad (Water)",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Lotad is said to have dwelled on land before. However, this Pokémon is thought to have returned to water because the leaf on its head grew large and heavy. It now lives by floating atop the water.",
        footer: "Tier 1 • [35-80%] • No. 270 / Base Set 1",
        img: "https://i.imgur.com/SVSYC7y.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/lotad.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  40   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Rain Dish',
                value: '<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.75</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with More<br><img class="icon" src="images/types/water.png">Water Types in Party</em>'
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    138: {
        name: "Lombre (Water)",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Lombre’s entire body is covered by a slippery, slimy film. It feels horribly unpleasant to be touched by this Pokémon’s hands. Lombre is often mistaken for a human child.",
        footer: "Tier 2 • [55-100%] • No. 271 / Base Set 1",
        img: "https://i.imgur.com/eyEkTlV.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/lombre.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  60   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Lilywater',
                value: '<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.75</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More<br><img class="icon" src="images/types/water.png">Water Types in Party</em>'
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    140: {
        name: "Lotad (Nature)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Lotad is said to have dwelled on land before. However, this Pokémon is thought to have returned to water because the leaf on its head grew large and heavy. It now lives by floating atop the water.",
        footer: "Tier 1 • [35-80%] • No. 270 / Base Set 1",
        img: "https://i.imgur.com/UABu59u.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/lotad.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  40   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Rain Dish',
                value: '<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.75</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with More<br><img class="icon" src="images/types/nature.png">Nature Types in Party</em>'
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    141: {
        name: "Lombre (Nature)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Lombre’s entire body is covered by a slippery, slimy film. It feels horribly unpleasant to be touched by this Pokémon’s hands. Lombre is often mistaken for a human child.",
        footer: "Tier 2 • [55-100%] • No. 271 / Base Set 1",
        img: "https://i.imgur.com/HfaOUnF.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/lombre.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  60   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Lilywater',
                value: '<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.75</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More<br><img class="icon" src="images/types/nature.png">Nature Types in Party</em>'
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    143: {
        name: "Seedot (Nature)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Seedot looks exactly like an acorn when it is dangling from a tree branch. It startles other Pokémon by suddenly moving. This Pokémon polishes its body once a day using leaves.",
        footer: "Tier 1 • [35-80%] • No. 273 / Base Set 1",
        img: "https://i.imgur.com/DewwXVz.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/seedot.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  40   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Seed of Doubt',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Earlier Slot</em><br><br><strong>5</strong>% 🌱 Leech Seed Infliction<br><strong>5</strong>% 💥 Flinch Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    144: {
        name: "Nuzleaf (Nature)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "This Pokémon pulls out the leaf on its head and makes a flute with it. The sound of Nuzleaf’s flute strikes fear and uncertainty in the hearts of people lost in a forest.",
        footer: "Tier 2 • [55-100%] • No. 274 / Base Set 1",
        img: "https://i.imgur.com/7ARmiWy.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/nuzleaf.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sinister Wood',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>5</strong>% 🌱 Leech Seed Infliction<br><strong>5</strong>% 💥 Flinch Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    146: {
        name: "Seedot (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Seedot looks exactly like an acorn when it is dangling from a tree branch. It startles other Pokémon by suddenly moving. This Pokémon polishes its body once a day using leaves.",
        footer: "Tier 1 • [35-80%] • No. 273 / Base Set 1",
        img: "https://i.imgur.com/gYeLkgQ.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/seedot.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  40   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Seed of Doubt',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Earlier Slot</em><br><br><strong>5</strong>% 🌱 Leech Seed Infliction<br><strong>5</strong>% 💥 Flinch Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    147: {
        name: "Nuzleaf (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "This Pokémon pulls out the leaf on its head and makes a flute with it. The sound of Nuzleaf’s flute strikes fear and uncertainty in the hearts of people lost in a forest.",
        footer: "Tier 2 • [55-100%] • No. 274 / Base Set 1",
        img: "https://i.imgur.com/YzdWUdy.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/nuzleaf.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sinister Wood',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>5</strong>% 🌱 Leech Seed Infliction<br><strong>5</strong>% 💥 Flinch Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    183: {
        name: "Wingull",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Wingull rides updrafts rising from the sea by extending its long and narrow wings to glide. This Pokémon’s long beak is useful for catching prey.",
        footer: "Tier 1 • [35-80%] • No. 278 / Base Set 1",
        img: "https://i.imgur.com/SZHy3iw.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/wingull.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  55   <strong>Def</strong>:  30"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Peck',
                value: "<strong>1</strong> PP 「2 Random Targets」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><br><strong>20</strong>% 💥 Flinch Infliction<br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    184: {
        name: "Pelipper",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Pelipper searches for food while in flight by skimming the wave tops. This Pokémon dips its large bill in the sea to scoop up food, then swallows everything in one big gulp.",
        footer: "Tier 2 • [55-100%] • No. 279 / Base Set 1",
        img: "https://i.imgur.com/FbIWen0.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pelipper.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  85   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Ocean Wind',
                value: "<strong>1</strong> PP 「2 Random Targets」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>35</strong>% 💥 Flinch Infliction<br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    150: {
        name: "Ralts (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Ralts has the ability to sense the emotions of people. If its Trainer is in a cheerful mood, this Pokémon grows cheerful and joyous in the same way.",
        footer: "Tier 1 • [35-80%] • No. 280 / Base Set 1",
        img: "https://i.imgur.com/t2BHxhx.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/ralts.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  28   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  45   <strong>Def</strong>:  35"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Inner Voice',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Earlier Slot</em><br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    151: {
        name: "Kirlia (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Kirlia uses the horns on its head to amplify its psychokinetic power. When the Pokémon uses its power, the air around it becomes distorted, creating mirages of nonexistent scenery.",
        footer: "Tier 2 • [55-100%] • No. 281 / Base Set 1",
        img: "https://i.imgur.com/glmblcN.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/kirlia.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  38   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fairy Pulse',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    154: {
        name: "Ralts (Fairy)",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "Ralts has the ability to sense the emotions of people. If its Trainer is in a cheerful mood, this Pokémon grows cheerful and joyous in the same way.",
        footer: "Tier 1 • [35-80%] • No. 280 / Base Set 1",
        img: "https://i.imgur.com/kYSirIU.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/ralts.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  28   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  45   <strong>Def</strong>:  35"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Inner Voice',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Earlier Slot</em><br><br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    155: {
        name: "Kirlia (Fairy)",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "Kirlia uses the horns on its head to amplify its psychokinetic power. When the Pokémon uses its power, the air around it becomes distorted, creating mirages of nonexistent scenery.",
        footer: "Tier 2 • [55-100%] • No. 281 / Base Set 1",
        img: "https://i.imgur.com/lczZ0rS.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/kirlia.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  38   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fairy Pulse',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    220: {
        name: "Aron",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Aron has a body of steel. With one all-out charge, this Pokémon can demolish even a heavy dump truck. The destroyed dump truck then becomes a handy meal for the Pokémon.",
        footer: "Tier 1 • [35-80%] • No. 304 / Base Set 1",
        img: "https://i.imgur.com/laEzEWs.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/aron.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Rubble',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Strongest in Slot <strong>3</strong></em><br><br><strong>20</strong>% ⚡ Paralyze Infliction<br><strong>5</strong>% 🌪 Sandstorm<br>⚠ +<strong>10</strong>% Critical Hit Rate"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong>'
            }
        ]
    },
    221: {
        name: "Lairon",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Lairon feeds on iron contained in rocks and water. It makes its nest on mountains where iron ore is buried. As a result, the Pokémon often clashes with humans mining the iron ore.",
        footer: "Tier 2 • [55-100%] • No. 305 / Base Set 1",
        img: "https://i.imgur.com/cV14yqH.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/lairon.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Mid<br><strong>Atk</strong>:  90   <strong>Def</strong>:  140"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Iron Quake',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Strongest in Slot <strong>3</strong></em><br><br><strong>20</strong>% ⚡ Paralyze Infliction<br><strong>5</strong>% 🌪 Sandstorm<br>⚠ +<strong>10</strong>% Critical Hit Rate"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>2</strong>'
            }
        ]
    },
    202: {
        name: "Plusle",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "When Plusle is cheering on its partner, it flashes with electric sparks from all over its body. If its partner loses, this Pokémon cries loudly.",
        footer: "Tier 2 • [55-100%] • No. 311 / Base Set 1",
        img: "https://i.imgur.com/E9D0gZN.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/plusle.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  85   <strong>Def</strong>:  75"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Helping Hand',
                value: "<strong>2</strong> PP 「2 Random Targets」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/electric.png"> Atk +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: 'With <strong>Minun</strong> in Party:<br>Permanent: <img class="icon" src="images/types/electric.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    203: {
        name: "Minun",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Minun loves to cheer on its partner in battle. It gives off sparks from its body while it is doing so. If its partner is in trouble, this Pokémon gives off increasing amounts of sparks.",
        footer: "Tier 2 • [55-100%] • No. 312 / Base Set 1",
        img: "https://i.imgur.com/3dbKN1c.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/minun.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  75   <strong>Def</strong>:  85"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Helping Hand',
                value: "<strong>2</strong> PP 「2 Random Targets」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/electric.png"> Enemy Def -<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: 'With <strong>Plusle</strong> in Party:<br>+<strong>20</strong>% Z-Move for all<img class="icon" src="images/types/electric.png">'
            }
        ]
    },
    88: {
        name: "Castform (Normal)",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Castform borrows the power of nature to transform itself into the guises of the sun, rain, and snow-clouds. This Pokémon’s feelings change with the weather.",
        footer: "Tier 2 • [55-100%] • No. 351 / Base Set 1",
        img: "https://i.imgur.com/0izmXQo.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/castform.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  70   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Cloud',
                value: "<strong>1</strong> PP<br><br>👥 +<strong>1</strong> Evasion"
            }
        ]
    },
    89: {
        name: "Castform (Sunny)",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Castform borrows the power of nature to transform itself into the guises of the sun, rain, and snow-clouds. This Pokémon’s feelings change with the weather.",
        footer: "Tier 2 • [55-100%] • No. 351 / Base Set 1",
        img: "https://i.imgur.com/oYde6zm.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/castform-sunny.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  70   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sunshine',
                value: "<strong>1</strong> PP<br><br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/ice.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>30</strong>% Z-Move for all<img class="icon" src="images/types/fire.png">'
            }
        ]
    },
    90: {
        name: "Castform (Rainy)",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Castform borrows the power of nature to transform itself into the guises of the sun, rain, and snow-clouds. This Pokémon’s feelings change with the weather.",
        footer: "Tier 2 • [55-100%] • No. 351 / Base Set 1",
        img: "https://i.imgur.com/IgbavFy.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/castform-rainy.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  70   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Rain',
                value: "<strong>1</strong> PP<br><br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>30</strong>% Z-Move for all<img class="icon" src="images/types/water.png">'
            }
        ]
    },
    91: {
        name: "Castform (Snowy)",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Castform borrows the power of nature to transform itself into the guises of the sun, rain, and snow-clouds. This Pokémon’s feelings change with the weather.",
        footer: "Tier 2 • [55-100%] • No. 351 / Base Set 1",
        img: "https://i.imgur.com/3zGvP99.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/castform-snowy.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  70   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Hail',
                value: "<strong>1</strong> PP<br><br><strong>5</strong>% ❄ Hail<br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>30</strong>% Z-Move for all<img class="icon" src="images/types/ice.png">'
            }
        ]
    },
    118: {
        name: "Absol",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "Absol has the ability to foretell the coming of natural disasters. It lives in a harsh, rugged mountain environment. This Pokémon very rarely ventures down from the mountains.",
        footer: "Tier 3 • [75-120%] • No. 359 / Base Set 1",
        img: "https://i.imgur.com/5tEknTu.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/absol.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  130   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Feint Attack',
                value: "<strong>4</strong> PP 「1 Random Target」<br>Multi:  x<strong>1.4</strong> ~ <strong>1.8</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases Per Knockout</em><br>Confuses your party 💫"
            },
            {
                name: '<span class="icon-num">1</span> Attack Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong><br><img class="icon" src="images/types/dark.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    120: {
        name: "Snorunt",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Snorunt survives by eating only snow and ice. Old folklore claims that a house visited by this Pokémon is sure to prosper for many generations to come.",
        footer: "Tier 1 • [35-80%] • No. 361 / Base Set 1",
        img: "https://i.imgur.com/JmlT7SQ.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/snorunt.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  50   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Snowball',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em><br><br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/ice.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/dragon.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/ice.png">'
            }
        ]
    },
    122: {
        name: "Glalie",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Glalie has the ability to freely control ice. For example, it can instantly freeze its prey solid. After immobilizing its prey in ice, this Pokémon enjoys eating it in leisurely fashion.",
        footer: "Tier 2 • [55-100%] • No. 362 / Base Set 1",
        img: "https://i.imgur.com/mxVRRTW.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/glalie.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  80   <strong>PP</strong>:  6   <strong>Wt</strong>: Heavy<br><strong>Atk</strong>:  80   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Ice Fang',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em><br><br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/ice.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/dragon.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/ice.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/ice.png">'
            }
        ]
    },
    121: {
        name: "Froslass",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Legends in snowy regions say that a woman who was lost on an icy mountain was reborn as Froslass.",
        footer: "Tier 2 • [55-100%] • No. 478 / Base Set 1",
        img: "https://i.imgur.com/0XGPo9W.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/froslass.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Cold Death',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Higher HP</em><br><br><strong>5</strong>% ❄ Hail<br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/ice.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/dragon.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong><br>+<strong>7</strong>% Z-Move for all<img class="icon" src="images/types/ice.png"><br>+<strong>7</strong>% Z-Move for all<img class="icon" src="images/types/psychic.png">'
            }
        ]
    },
    217: {
        name: "Spheal",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Spheal always travels by rolling around on its ball-like body. When the season for ice floes arrives, this Pokémon can be seen rolling about on ice and crossing the sea.",
        footer: "Tier 1 • [35-80%] • No. 363 / Base Set 1",
        img: "https://i.imgur.com/KPjMfnz.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/spheal.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  55   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sleet',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Earlier Slot</em><br><br><strong>5</strong>% 💥 Flinch Infliction<br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    218: {
        name: "Sealeo",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Sealeo often balances and rolls things on the tip of its nose. While the Pokémon is rolling something, it checks the object’s aroma and texture to determine whether it likes the object or not.",
        footer: "Tier 2 • [55-100%] • No. 364 / Base Set 1",
        img: "https://i.imgur.com/HE4F9au.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/sealeo.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  90   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  75   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Freezing Rain',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>5</strong>% 💥 Flinch Infliction<br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    125: {
        name: "Bagon",
        desc: '<img class="icon" src="images/types/dragon.png">Dragon Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png">',
        bio: "Bagon harbors a never-ending dream of one day soaring high among the clouds. As if trying to dispel its frustration over its inability to fly, this Pokémon slams its hard head against huge rocks and shatters them into pebbles.",
        footer: "Tier 1 • [35-80%] • No. 371 / Base Set 1",
        img: "https://i.imgur.com/SJkpvOE.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/bagon.gif",
        type: 10,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  75   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Dragon Claw',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em>"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/dragon.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/electric.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/dragon.png">'
            }
        ]
    },
    126: {
        name: "Shelgon",
        desc: '<img class="icon" src="images/types/dragon.png">Dragon Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png">',
        bio: "Covering Shelgon’s body are outgrowths much like bones. The shell is very hard and bounces off enemy attacks. When awaiting evolution, this Pokémon hides away in a cavern.",
        footer: "Tier 2 • [55-100%] • No. 372 / Base Set 1",
        img: "https://i.imgur.com/lLjeUlC.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/shelgon.gif",
        type: 10,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  6   <strong>Wt</strong>: Mid<br><strong>Atk</strong>:  95   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Dragon Tail',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em>"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/dragon.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/electric.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/dragon.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/dragon.png">'
            }
        ]
    },
    156: {
        name: "Beldum (Earth)",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Beldum keeps itself floating by generating a magnetic force that repels earth’s natural magnetism. When it sleeps, this Pokémon anchors itself to a cliff using the hooks on its rear.",
        footer: "Tier 1 • [35-80%] • No. 374 / Base Set 1",
        img: "https://i.imgur.com/C0VZLeG.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/beldum.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  55   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Levitate',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Later Slot</em><br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '3 Turn: <img class="icon" src="images/types/earth.png"> Def +<strong>1</strong>'
            }
        ]
    },
    157: {
        name: "Metang (Earth)",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "When two Beldum fuse together, Metang is formed. The brains of the Beldum are joined by a magnetic nervous system. This Pokémon turns its arms to the rear for traveling at high speed.",
        footer: "Tier 2 • [55-100%] • No. 375 / Base Set 1",
        img: "https://i.imgur.com/7HM1Xed.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/metang.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Heavy<br><strong>Atk</strong>:  75   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Metal Claw',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Later Slot</em><br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '3 Turn: <img class="icon" src="images/types/earth.png"> Def +<strong>1</strong>'
            }
        ]
    },
    160: {
        name: "Beldum (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Beldum keeps itself floating by generating a magnetic force that repels earth’s natural magnetism. When it sleeps, this Pokémon anchors itself to a cliff using the hooks on its rear.",
        footer: "Tier 1 • [35-80%] • No. 374 / Base Set 1",
        img: "https://i.imgur.com/Gyso2gO.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/beldum.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  55   <strong>Def</strong>:  80"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Levitate',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Later Slot</em><br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '3 Turn: <img class="icon" src="images/types/earth.png"> Def +<strong>1</strong>'
            }
        ]
    },
    161: {
        name: "Metang (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "When two Beldum fuse together, Metang is formed. The brains of the Beldum are joined by a magnetic nervous system. This Pokémon turns its arms to the rear for traveling at high speed.",
        footer: "Tier 2 • [55-100%] • No. 375 / Base Set 1",
        img: "https://i.imgur.com/omoToNp.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/metang.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Heavy<br><strong>Atk</strong>:  75   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Metal Claw',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Later Slot</em><br><br><strong>3</strong>% 💫 Confusion Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '3 Turn: <img class="icon" src="images/types/earth.png"> Def +<strong>1</strong>'
            }
        ]
    },
    187: {
        name: "Starly",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "They flock around mountains and fields, chasing after bug Pokémon. Their singing is noisy and annoying.",
        footer: "Tier 1 • [35-80%] • No. 396 / Base Set 1",
        img: "https://i.imgur.com/XJK7qtN.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/starly.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  55   <strong>Def</strong>:  30"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sky Sortie',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><br>👥 +<strong>1</strong> Evasion<br>🎯 -<strong>1</strong> Enemy Accuracy<br>👥 -<strong>1</strong> Enemy Evasion"
            }
        ]
    },
    176: {
        name: "Bidoof",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "It constantly gnaws on logs and rocks to whittle down its front teeth. It nests alongside water.",
        footer: "Tier 1 • [35-80%] • No. 399 / Base Set 1",
        img: "https://i.imgur.com/I5uJBZL.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/bidoof.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  59   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  45   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Nibble',
                value: "<strong>3</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><br>💬 Dispel Enemy Buffs"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    177: {
        name: "Bibarel",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "It makes its nest by damming streams with bark and mud. It is known as an industrious worker.",
        footer: "Tier 2 • [55-100%] • No. 400 / Base Set 1",
        img: "https://i.imgur.com/d5LVJxH.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/bibarel.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  79   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  85   <strong>Def</strong>:  71"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Beaver Bite',
                value: "<strong>3</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br>💬 Dispel Enemy Buffs"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong>'
            }
        ]
    },
    116: {
        name: "Shinx",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "All of its fur dazzles if danger is sensed. It flees while the foe is momentarily blinded.",
        footer: "Tier 1 • [35-80%] • No. 403 / Base Set 1",
        img: "https://i.imgur.com/MGwFWPb.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/shinx.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  34"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Wild Shock',
                value: "<strong>1</strong> PP 「1 Random Target」<br>Multi:  x<strong>1.0</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Later Slot</em><br><br><strong>5</strong>% 🔥 Burn Infliction<br><strong>10</strong>% ⚡ Paralyze Infliction"
            }
        ]
    },
    117: {
        name: "Luxio",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Strong electricity courses through the tips of its sharp claws. A light scratch causes fainting in foes.",
        footer: "Tier 2 • [55-100%] • No. 404 / Base Set 1",
        img: "https://i.imgur.com/d51iZpp.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/luxio.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  85   <strong>Def</strong>:  49"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Wild Lightning',
                value: "<strong>2</strong> PP 「1 Random Target」<br>Multi:  x<strong>1.0</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Later Slot</em><br><br><strong>10</strong>% 🔥 Burn Infliction<br><strong>15</strong>% ⚡ Paralyze Infliction"
            }
        ]
    },
    99: {
        name: "Burmy (Plant)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "If its cloak is broken in battle, it quickly remakes the cloak with materials nearby.",
        footer: "Tier 1 • [35-80%] • No. 412 / Base Set 1",
        img: "https://i.imgur.com/HzoRNsL.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/burmy.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  29   <strong>Def</strong>:  45"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Plant Cloak',
                value: "<strong>2</strong> PP"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/nature.png"> Def +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/nature.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    102: {
        name: "Wormadam (Plant)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "When Burmy evolved, its cloak became a part of this Pokémon’s body. The cloak is never shed.",
        footer: "Tier 2 • [55-100%] • No. 413 / Base Set 1",
        img: "https://i.imgur.com/cnTXlEe.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/wormadam.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  79   <strong>Def</strong>:  105"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Plant Cloak+',
                value: "<strong>2</strong> PP"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/nature.png"> Def +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '2 Turn: <img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/nature.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    100: {
        name: "Burmy (Sandy)",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "If its cloak is broken in battle, it quickly remakes the cloak with materials nearby.",
        footer: "Tier 1 • [35-80%] • No. 412 / Base Set 1",
        img: "https://i.imgur.com/HeZudO5.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/burmy-sandy.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  29   <strong>Def</strong>:  45"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sandy Cloak',
                value: "<strong>2</strong> PP<br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/earth.png"> Def +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/earth.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    103: {
        name: "Wormadam (Sandy)",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "When Burmy evolved, its cloak became a part of this Pokémon’s body. The cloak is never shed.",
        footer: "Tier 2 • [55-100%] • No. 413 / Base Set 1",
        img: "https://i.imgur.com/AwYENIZ.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/wormadam-sandy.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  79   <strong>Def</strong>:  105"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Sandy Cloak+',
                value: "<strong>2</strong> PP<br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/earth.png"> Def +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '2 Turn: <img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/earth.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    101: {
        name: "Burmy (Trash)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "If its cloak is broken in battle, it quickly remakes the cloak with materials nearby.",
        footer: "Tier 1 • [35-80%] • No. 412 / Base Set 1",
        img: "https://i.imgur.com/moJ9hd2.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/burmy-trash.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  29   <strong>Def</strong>:  45"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Trash Cloak',
                value: "<strong>2</strong> PP"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/dark.png"> Def +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/dark.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    104: {
        name: "Wormadam (Trash)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "When Burmy evolved, its cloak became a part of this Pokémon’s body. The cloak is never shed.",
        footer: "Tier 2 • [55-100%] • No. 413 / Base Set 1",
        img: "https://i.imgur.com/bHJcOLs.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/wormadam-trash.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  79   <strong>Def</strong>:  105"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Trash Cloak+',
                value: "<strong>2</strong> PP"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/dark.png"> Def +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '2 Turn: <img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/dark.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    174: {
        name: "Combee",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "It collects and delivers honey to its colony. At night, they cluster to form a beehive and sleep.",
        footer: "Tier 1 • [35-80%] • No. 415 / Base Set 1",
        img: "https://i.imgur.com/Y6gesza.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/combee.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  30   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  30   <strong>Def</strong>:  42"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Hive Wall',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><br><strong>30</strong>% 🍄 Poison Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            }
        ]
    },
    175: {
        name: "Vespiquen",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Its abdomen is a honeycomb for grubs. It raises its grubs on honey collected by Combee.",
        footer: "Tier 2 • [55-100%] • No. 416 / Base Set 1",
        img: "https://i.imgur.com/jEmAWnp.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/vespiquen.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  70   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  80   <strong>Def</strong>:  102"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Hive Wall+',
                value: "<strong>3</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>30</strong>% 🍄 Poison Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            }
        ]
    },
    214: {
        name: "Pachirisu",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"> <strong>Paralyzed</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "A pair may be seen rubbing their cheek pouches together in an effort to share stored electricity.",
        footer: "Tier 2 • [55-100%] • No. 417 / Base Set 1",
        img: "https://i.imgur.com/uFnq6to.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pachirisu.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  45   <strong>Def</strong>:  90"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Piercing Volt',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Fewer Enemies</em><br><strong>Recoil!</strong> Lose all but <strong>1</strong> HP<br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    179: {
        name: "Buizel",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "It inflates the flotation sac around its neck and pokes its head out of the water to see what is going on.",
        footer: "Tier 1 • [35-80%] • No. 418 / Base Set 1",
        img: "https://i.imgur.com/U6mqzQG.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/buizel.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  35"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Water Tackle',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    180: {
        name: "Floatzel",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Its flotation sac developed as a result of pursuing aquatic prey. It can double as a rubber raft.",
        footer: "Tier 2 • [55-100%] • No. 419 / Base Set 1",
        img: "https://i.imgur.com/irhoPso.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/floatzel.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  85   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  105   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Crushing Wave',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.54</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    78: {
        name: "Chatot",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "It can learn and speak human words. If they gather, they all learn the same saying.",
        footer: "Tier 2 • [55-100%] • No. 441 / Base Set 1",
        img: "https://i.imgur.com/4mD1r8Q.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/chatot.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  76   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  92   <strong>Def</strong>:  45"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Chatter',
                value: "<strong>1</strong> PP 「3 Random Targets」<br>Multi:  x<strong>0.5</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>100</strong>% 💫 Confusion Infliction"
            }
        ]
    },
    127: {
        name: "Sandile",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "They live buried in the sands of the desert. The sun-warmed sands prevent their body temperature from dropping.",
        footer: "Tier 1 • [35-80%] • No. 551 / Base Set 1",
        img: "https://i.imgur.com/3Odj8Ep.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/sandile.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  72   <strong>Def</strong>:  35"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Pursuit',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Per Knockout</em>"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/psychic.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>5</strong>% Z-Move for all<img class="icon" src="images/types/dark.png">'
            }
        ]
    },
    128: {
        name: "Krokorok",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "The special membrane covering its eyes can sense the heat of objects, so it can see its surroundings even in darkness.",
        footer: "Tier 2 • [55-100%] • No. 552 / Base Set 1",
        img: "https://i.imgur.com/CZmT4Ou.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/krokorok.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  82   <strong>Def</strong>:  45"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Foul Play',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Per Knockout</em>"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong><br><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/psychic.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/dark.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>10</strong>% Z-Move for all<img class="icon" src="images/types/dark.png">'
            }
        ]
    },
    49: {
        name: "Minccino",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "These Pokémon prefer a tidy habitat. They are always sweeping and dusting, using their tails as brooms.",
        footer: "Tier 2 • [55-100%] • No. 572 / Base Set 1",
        img: "https://i.imgur.com/Qkjz9x5.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/minccino.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  50   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Encore',
                value: "<strong>1</strong> PP"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    50: {
        name: "Deerling (Spring)",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "The turning of the seasons changes the color and scent of this Pokémon's fur. People use it to mark the seasons.",
        footer: "Tier 2 • [55-100%] • No. 585 / Base Set 1",
        img: "https://i.imgur.com/wGEdLsI.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/deerling.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  60   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Nature\'s Gift',
                value: "<strong>1</strong> PP"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/rainbow.png">+<strong>1</strong> PP<br><img class="icon" src="images/types/fairy.png">+<strong>2</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    51: {
        name: "Deerling (Summer)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "The turning of the seasons changes the color and scent of this Pokémon's fur. People use it to mark the seasons.",
        footer: "Tier 2 • [55-100%] • No. 585 / Base Set 1",
        img: "https://i.imgur.com/L0RSHBU.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/deerling-summer.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  60   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Nature\'s Gift',
                value: "<strong>1</strong> PP"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/rainbow.png">+<strong>1</strong> PP<br><img class="icon" src="images/types/nature.png">+<strong>2</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    52: {
        name: "Deerling (Autumn)",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "The turning of the seasons changes the color and scent of this Pokémon's fur. People use it to mark the seasons.",
        footer: "Tier 2 • [55-100%] • No. 585 / Base Set 1",
        img: "https://i.imgur.com/sApiLBq.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/deerling-autumn.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  60   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Nature\'s Gift',
                value: "<strong>1</strong> PP<br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/rainbow.png">+<strong>1</strong> PP<br><img class="icon" src="images/types/earth.png">+<strong>2</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    53: {
        name: "Deerling (Winter)",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "The turning of the seasons changes the color and scent of this Pokémon's fur. People use it to mark the seasons.",
        footer: "Tier 2 • [55-100%] • No. 585 / Base Set 1",
        img: "https://i.imgur.com/i2do7Id.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/deerling-winter.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  2   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  60   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Nature\'s Gift',
                value: "<strong>1</strong> PP<br><br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/rainbow.png">+<strong>1</strong> PP<br><img class="icon" src="images/types/ice.png">+<strong>2</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    166: {
        name: "Cubchoo",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "Their snot is a barometer of health. When healthy, their snot is sticky and the power of their ice moves increases.",
        footer: "Tier 2 • [55-100%] • No. 613 / Base Set 1",
        img: "https://i.imgur.com/SjHIKr4.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/cubchoo.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Powder Snow',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>10</strong>% ⚡ Paralyze Infliction<br><strong>5</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    227: {
        name: "Deino",
        desc: '<img class="icon" src="images/types/dragon.png">Dragon Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png">',
        bio: "Lacking sight, it’s unaware of its surroundings, so it bumps into things and eats anything that moves.",
        footer: "Tier 1 • [35-80%] • No. 633 / Base Set 1",
        img: "https://i.imgur.com/rjEjzRM.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/deino.gif",
        type: 10,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  52   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  50"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Dark Drake',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong> ~ <strong>1.96</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases Each Turn</em>"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    35: {
        name: "Fletchling",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "Despite the beauty of its lilting voice, it’s merciless to intruders that enter its territory.",
        footer: "Tier 1 • [35-80%] • No. 661 / Base Set 1",
        img: "https://i.imgur.com/1QonLyd.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/fletchling.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  50   <strong>Def</strong>:  43"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Peck',
                value: "<strong>1</strong> PP 「2 Random Targets」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><br><strong>20</strong>% 💥 Flinch Infliction<br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    36: {
        name: "Fletchinder",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "The hotter the flame sac on its belly, the faster it can fly, but it takes some time to get the fire going.",
        footer: "Tier 2 • [55-100%] • No. 662 / Base Set 1",
        img: "https://i.imgur.com/Mo1kjXr.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/fletchinder.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  62   <strong>PP</strong>:  3   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  73   <strong>Def</strong>:  55"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Burning Wind',
                value: "<strong>1</strong> PP 「2 Random Targets」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>10</strong>% 🔥 Burn Infliction<br><strong>30</strong>% 💥 Flinch Infliction<br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    188: {
        name: "Scatterbug",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "The powder that covers its body regulates its temperature, so it can live in any region or climate.",
        footer: "Tier 1 • [35-80%] • No. 664 / Base Set 1",
        img: "https://i.imgur.com/CKJynrM.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/scatterbug.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  38   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  35   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Paralyze Powder',
                value: "<strong>1</strong> PP 「3 Random Targets」<br>Multi:  x<strong>0.5</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Earlier Slot</em><br><br><strong>100</strong>% ⚡ Paralyze Infliction"
            }
        ]
    },
    213: {
        name: "Spewpa",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "The beaks of bird Pokémon can’t begin to scratch its stalwart body. To defend itself, it spews powder.",
        footer: "Tier 2 • [55-100%] • No. 665 / Base Set 1",
        img: "https://i.imgur.com/f4nB6B1.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/spewpa.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  27   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Harden',
                value: "<strong>1</strong> PP"
            },
            {
                name: '<span class="icon-num">4</span> Turn Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong>'
            }
        ]
    },
    25: {
        name: "Litleo",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "They set off on their own from their pride and live by themselves to become stronger. These hot-blooded Pokémon are quick to fight.",
        footer: "Tier 2 • [55-100%] • No. 667 / Base Set 1",
        img: "https://i.imgur.com/EHKbDRE.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/litleo.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  62   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  73   <strong>Def</strong>:  58"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Lion\'s Pride',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/fire.png"> Atk +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: "<em>Self:</em> +<strong>2</strong> PP<br><em>Slot 5:</em> +<strong>2</strong> PP"
            }
        ]
    },
    207: {
        name: "Flabébé",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"> <strong>Sleeping</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "When it finds a flower it likes, it dwells on that flower its whole life long. It floats in the wind’s embrace with an untroubled heart.",
        footer: "Tier 1 • [35-80%] • No. 669 / Base Set 1",
        img: "https://i.imgur.com/RRxkv9Q.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/flabebe.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  44   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  61   <strong>Def</strong>:  79"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Petal Curse',
                value: "<strong>1</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><em>Increases with Fewer Enemies</em><br><strong>Recoil!</strong> Lose all but <strong>1</strong> HP<br><br><strong>5</strong>% 💤 Sleep Infliction<br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    208: {
        name: "Floette",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"> <strong>Sleeping</strong> Pokémon<br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "When the flowers of a well-tended flower bed bloom, it appears and celebrates with an elegant dance.",
        footer: "Tier 2 • [55-100%] • No. 670 / Base Set 1",
        img: "https://i.imgur.com/H0u1f6I.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/floette.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  54   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  75   <strong>Def</strong>:  98"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Wither',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Fewer Enemies</em><br><strong>Recoil!</strong> Lose all but <strong>1</strong> HP<br><br><strong>10</strong>% 💤 Sleep Infliction<br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    211: {
        name: "Eternal Floette (Fairy)",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "When the flowers of a well-tended flower bed bloom, it appears and celebrates with an elegant dance.",
        footer: "Tier 3 • [75-120%] • No. 670 / Base Set 1",
        img: "https://i.imgur.com/UE9h3ZE.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/floette-eternal.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  54   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  75   <strong>Def</strong>:  98"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Light of Ruin',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.3</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Higher HP</em><br><strong>Recoil!</strong> Lose <strong>25</strong>% of max HP<br><br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">3</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/dark.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>7</strong>% Z-Move for all<img class="icon" src="images/types/fairy.png"><br>+<strong>7</strong>% Z-Move for all<img class="icon" src="images/types/dark.png">'
            }
        ]
    },
    212: {
        name: "Eternal Floette (Dark)",
        desc: '<img class="icon" src="images/types/dark.png">Dark Type<br><em>Strong Against:</em> <img class="icon" src="images/types/psychic.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png">',
        bio: "When the flowers of a well-tended flower bed bloom, it appears and celebrates with an elegant dance.",
        footer: "Tier 3 • [75-120%] • No. 670 / Base Set 1",
        img: "https://i.imgur.com/dICdrjS.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/floette-eternal.gif",
        type: 9,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  54   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  75   <strong>Def</strong>:  98"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Light of Ruin',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.85</strong> ~ <strong>1.3</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Higher HP</em><br><strong>Recoil!</strong> Lose <strong>25</strong>% of max HP"
            },
            {
                name: '<span class="icon-num">3</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/fairy.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/dark.png"> Def +<strong>1</strong><br><img class="icon" src="images/types/fairy.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '+<strong>7</strong>% Z-Move for all<img class="icon" src="images/types/fairy.png"><br>+<strong>7</strong>% Z-Move for all<img class="icon" src="images/types/dark.png">'
            }
        ]
    },
    199: {
        name: "Skiddo",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "If it has sunshine and water, it doesn’t need to eat, because it can generate energy from the leaves on its back.",
        footer: "Tier 2 • [55-100%] • No. 672 / Base Set 1",
        img: "https://i.imgur.com/Xi6Qyqa.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/skiddo.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  66   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  57"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Foal Play',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>20</strong>% 🌱 Leech Seed Infliction<br><strong>5</strong>% 💥 Flinch Infliction"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    200: {
        name: "Gogoat",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "They inhabit mountainous regions. The leader of the herd is decided by a battle of clashing horns.",
        footer: "Tier 3 • [75-120%] • No. 673 / Base Set 1",
        img: "https://i.imgur.com/E2rfqQJ.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/gogoat.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  123   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  100   <strong>Def</strong>:  81"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Healing Hoof',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><br><strong>30</strong>% 🌱 Leech Seed Infliction<br><strong>5</strong>% 💥 Flinch Infliction"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/nature.png"> Atk +<strong>2</strong>'
            }
        ]
    },
    189: {
        name: "Pancham",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "It does its level best to glare and pull a scary face, but it can’t help grinning if anyone pats its head.",
        footer: "Tier 2 • [55-100%] • No. 674 / Base Set 1",
        img: "https://i.imgur.com/W2E9tXq.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pancham.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  67   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  82   <strong>Def</strong>:  62"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Scrap',
                value: '<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.68</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with More<br><img class="icon" src="images/types/dark.png">Dark Types in Party</em><br><strong>Recoil!</strong> Lose <strong>20</strong>% of max HP<br><br><strong>10</strong>% ⚡ Paralyze Infliction<br><strong>20</strong>% 💥 Flinch Infliction<br><strong>5</strong>% 🌪 Sandstorm'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dark.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    226: {
        name: "Espurr",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "It has enough psychic energy to blast everything within 300 feet of itself, but it has no control over its power.",
        footer: "Tier 2 • [55-100%] • No. 677 / Base Set 1",
        img: "https://i.imgur.com/QtHzwjL.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/espurr.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  62   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  63   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Keeping Pace',
                value: "<strong>1</strong> PP"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/normal.png"><img class="icon" src="images/types/rainbow.png"> Atk +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '2 Turn: <img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    224: {
        name: "Meowstic (Male)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "The eyeball patterns on the interior of its ears emit psychic energy. It keeps the patterns tightly covered because that power is too immense.",
        footer: "Tier 3 • [75-120%] • No. 678 / Base Set 1",
        img: "https://i.imgur.com/YocT5xi.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/meowstic.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  74   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  83   <strong>Def</strong>:  81"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Psionic Bond',
                value: "<strong>2</strong> PP 「2 Random Targets」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><br><strong>3</strong>% 💫 Confusion Infliction<br><strong>20</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/psychic.png"> Atk +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: 'With <strong>Meowstic (Female)</strong> in Party:<br>Permanent: <img class="icon" src="images/types/psychic.png"> Enemy Def -<strong>2</strong>'
            }
        ]
    },
    225: {
        name: "Meowstic (Female)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "The eyeball patterns on the interior of its ears emit psychic energy. It keeps the patterns tightly covered because that power is too immense.",
        footer: "Tier 3 • [75-120%] • No. 678 / Base Set 1",
        img: "https://i.imgur.com/SXfyk3E.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/meowstic-f.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  74   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  83   <strong>Def</strong>:  81"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Psionic Bond',
                value: "<strong>2</strong> PP 「2 Random Targets」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><br><strong>3</strong>% 💫 Confusion Infliction<br><strong>20</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">3</span> Attack Buff',
                value: '<img class="icon" src="images/types/psychic.png"> Enemy Def -<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: 'With <strong>Meowstic (Male)</strong> in Party:<br>+<strong>20</strong>% Z-Move for all<img class="icon" src="images/types/psychic.png">'
            }
        ]
    },
    201: {
        name: "Skrelp",
        desc: '<img class="icon" src="images/types/dragon.png">Dragon Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png">',
        bio: "It looks just like rotten kelp. It hides from foes while storing up power for its evolution.",
        footer: "Tier 2 • [55-100%] • No. 690 / Base Set 1",
        img: "https://i.imgur.com/yBQq6js.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/skrelp.gif",
        type: 10,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  50   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  60   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Toxic Waters',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>5</strong>% 🍄 Poison Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    215: {
        name: "Helioptile",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "The frills on either side of its head have cells that generate electricity when exposed to sunlight.",
        footer: "Tier 2 • [55-100%] • No. 694 / Base Set 1",
        img: "https://i.imgur.com/6xONDT4.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/helioptile.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  44   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  61   <strong>Def</strong>:  43"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Quick Jolt',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/electric.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/electric.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    216: {
        name: "Heliolisk",
        desc: '<img class="icon" src="images/types/electric.png">Electric Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/dragon.png">',
        bio: "It stimulates its muscles with electricity, boosting the strength in its legs and enabling it to run 100 yards in five seconds.",
        footer: "Tier 3 • [75-120%] • No. 695 / Base Set 1",
        img: "https://i.imgur.com/eoHlYEG.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/heliolisk.gif",
        type: 5,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  62   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  109   <strong>Def</strong>:  94"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Electrify',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><br><strong>5</strong>% ⚡ Paralyze Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/electric.png"> Enemy Def -<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/electric.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    204: {
        name: "Tyrunt",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "Its immense jaws have enough destructive force that it can chew up an automobile. It lived 100 million years ago.",
        footer: "Tier 2 • [55-100%] • No. 696 / Base Set 1",
        img: "https://i.imgur.com/RrsvzGa.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/tyrunt.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  58   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  89   <strong>Def</strong>:  77"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Prehistoric Quake',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>50</strong>% 🌪 Sandstorm"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    169: {
        name: "Amaura",
        desc: '<img class="icon" src="images/types/ice.png">Ice Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/ice.png">',
        bio: "This calm Pokémon lived in a cold land where there were no violent predators like Tyrantrum.",
        footer: "Tier 2 • [55-100%] • No. 698 / Base Set 1",
        img: "https://i.imgur.com/w5YGxc6.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/amaura.gif",
        type: 6,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  77   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  67   <strong>Def</strong>:  63"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Arctic Tundra',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases w/ More Moves<br>Used This Turn</em><br><br><strong>50</strong>% ❄ Hail"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/ice.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    95: {
        name: "Phantump (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "According to old tales, these Pokémon are stumps possessed by the spirits of children who died while lost in the forest.",
        footer: "Tier 2 • [55-100%] • No. 708 / Base Set 1",
        img: "https://i.imgur.com/FcpHgxR.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/phantump.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  43   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Scary Woods',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Each Turn</em><br><br><strong>3</strong>% 💫 Confusion Infliction<br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    96: {
        name: "Trevenant (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "Using its roots as a nervous system, it controls the trees in the forest. It’s kind to the Pokémon that reside in its body.",
        footer: "Tier 3 • [75-120%] • No. 709 / Base Set 1",
        img: "https://i.imgur.com/wnjryqc.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/trevenant.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  85   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  110   <strong>Def</strong>:  82"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Haunted Hollow',
                value: "<strong>3</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases Each Turn</em><br><br><strong>3</strong>% 💫 Confusion Infliction<br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    97: {
        name: "Phantump (Nature)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "According to old tales, these Pokémon are stumps possessed by the spirits of children who died while lost in the forest.",
        footer: "Tier 2 • [55-100%] • No. 708 / Base Set 1",
        img: "https://i.imgur.com/Y8BbPzg.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/phantump.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  43   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Scary Woods',
                value: "<strong>2</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases Each Turn</em><br><br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    98: {
        name: "Trevenant (Nature)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Using its roots as a nervous system, it controls the trees in the forest. It’s kind to the Pokémon that reside in its body.",
        footer: "Tier 3 • [75-120%] • No. 709 / Base Set 1",
        img: "https://i.imgur.com/HhbgHnI.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/trevenant.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  85   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  110   <strong>Def</strong>:  82"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Haunted Hollow',
                value: "<strong>3</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases Each Turn</em><br><br>👥 +<strong>1</strong> Evasion"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    178: {
        name: "Pikipek",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "This Pokémon feeds on berries, whose leftover seeds become the ammunition for the attacks it fires off from its mouth.",
        footer: "Tier 1 • [35-80%] • No. 731 / Base Set 1",
        img: "https://i.imgur.com/NekFLFm.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/pikipek.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  35   <strong>PP</strong>:  3   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  75   <strong>Def</strong>:  30"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Peck',
                value: "<strong>1</strong> PP 「Single Target」<br><strong>8</strong> Fixed Damage<br>Multi:  x<strong>1.4</strong><br>Z-Move:  x<strong>1.8</strong>  [+80%]<br><br>👥 +<strong>1</strong> Evasion<br>⚠ +<strong>10</strong>% Critical Hit Rate"
            },
            {
                name: "💛 PP Restore",
                value: '<img class="icon" src="images/types/rainbow.png">+<strong>1</strong> PP<br><em>Does Not Target Self</em>'
            }
        ]
    },
    148: {
        name: "Cutiefly",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "Myriads of Cutiefly flutter above the heads of people who have auras resembling those of flowers.",
        footer: "Tier 2 • [55-100%] • No. 742 / Base Set 1",
        img: "https://i.imgur.com/mpB7gkC.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/cutiefly.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  55   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fairy Pollen',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Stronger against lighter foes</em><br><br><strong>5</strong>% 🍄 Poison Infliction<br><strong>5</strong>% ⚡ Paralyze Infliction<br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    149: {
        name: "Ribombee",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "Some of Ribombee’s pollen puffs are highly nutritious. They are sometimes sold as supplements.",
        footer: "Tier 3 • [75-120%] • No. 743 / Base Set 1",
        img: "https://i.imgur.com/8gem6YF.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/ribombee.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  95   <strong>Def</strong>:  70"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fairy Sting',
                value: "<strong>4</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.65</strong> ~ <strong>1.0</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Stronger against lighter foes</em><br><br><strong>5</strong>% 🍄 Poison Infliction<br><strong>5</strong>% ⚡ Paralyze Infliction<br><strong>3</strong>% 💕 Charm Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    222: {
        name: "Rockruff",
        desc: '<img class="icon" src="images/types/earth.png">Earth Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/electric.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/psychic.png">',
        bio: "This Pokémon has lived with people since times long ago. It can sense when its Trainer is in the dumps and will stick close by its Trainer’s side.",
        footer: "Tier 2 • [55-100%] • No. 744 / Base Set 1",
        img: "https://i.imgur.com/b7BMaTv.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/rockruff.gif",
        type: 4,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  45   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  65   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Puppy Play',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>5</strong>% 🌪 Sandstorm"
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/earth.png"> Atk +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: "<em>Self:</em> +<strong>2</strong> PP<br><em>Slot 5:</em> +<strong>2</strong> PP"
            }
        ]
    },
    185: {
        name: "Dewpider",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "When it comes across enemies or potential prey, this Pokémon smashes its water-bubble-covered head into them.",
        footer: "Tier 2 • [55-100%] • No. 751 / Base Set 1",
        img: "https://i.imgur.com/voK91yD.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/dewpider.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  38   <strong>PP</strong>:  5   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  40   <strong>Def</strong>:  72"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Water Web',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Earlier Slot</em><br><br><strong>10</strong>% 🍄 Poison Infliction<br>👥 -<strong>1</strong> Enemy Evasion"
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/water.png"> Atk +<strong>1</strong>'
            },
            {
                name: "💛 PP Restore",
                value: "<em>Self:</em> +<strong>2</strong> PP<br><em>Slot 5:</em> +<strong>2</strong> PP"
            }
        ]
    },
    186: {
        name: "Araquanid",
        desc: '<img class="icon" src="images/types/water.png">Water Type<br><em>Strong Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Despite what its appearance suggests, it cares for others. If it finds vulnerable, weak Pokémon, it protectively brings them into its water bubble.",
        footer: "Tier 3 • [75-120%] • No. 752 / Base Set 1",
        img: "https://i.imgur.com/DPQlo0X.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/araquanid.gif",
        type: 2,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  68   <strong>PP</strong>:  5   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  70   <strong>Def</strong>:  132"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Water Web+',
                value: "<strong>2</strong> PP 「<strong>AoE</strong>」<br>Multi:  x<strong>0.7</strong> ~ <strong>1.25</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Earlier Slot</em><br><br><strong>15</strong>% 🍄 Poison Infliction<br>👥 -<strong>2</strong> Enemy Evasion"
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '1 Turn: <img class="icon" src="images/types/water.png"> Atk +<strong>2</strong>'
            },
            {
                name: "💛 PP Restore",
                value: "<em>Self:</em> +<strong>2</strong> PP<br><em>Slot 5:</em> +<strong>3</strong> PP"
            }
        ]
    },
    172: {
        name: "Morelull",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "As it drowses the day away, it nourishes itself by sucking from tree roots. It wakens at the fall of night, wandering off in search of a new tree.",
        footer: "Tier 2 • [55-100%] • No. 755 / Base Set 1",
        img: "https://i.imgur.com/fZAChls.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/morelull.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  40   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  65   <strong>Def</strong>:  75"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Dazzling Shroom',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Higher HP</em><br><br><strong>20</strong>% 🍄 Poison Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    173: {
        name: "Shiinotic",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "It emits flickering spores that cause drowsiness. When its prey succumb to sleep, this Pokémon feeds on them by sucking in their energy.",
        footer: "Tier 3 • [75-120%] • No. 756 / Base Set 1",
        img: "https://i.imgur.com/rlDNcz1.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/shiinotic.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  90   <strong>Def</strong>:  100"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Fairy Spore',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Higher HP</em><br><br><strong>20</strong>% 🍄 Poison Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/fairy.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    31: {
        name: "Salandit (Nature)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Volcanoes or dry, craggy places are its home. It emanates a sweet-smelling poisonous gas that attracts bug Pokémon, then attacks them.",
        footer: "Tier 2 • [55-100%] • No. 757 / Base Set 1",
        img: "https://i.imgur.com/5PvS2oP.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/salandit.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  48   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  71   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Smolder',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Higher PP</em><br><br><strong>5</strong>% 🍄 Poison Infliction<br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    32: {
        name: "Salazzle (Nature)",
        desc: '<img class="icon" src="images/types/nature.png">Nature Type<br><em>Strong Against:</em> <img class="icon" src="images/types/water.png"><img class="icon" src="images/types/earth.png"><img class="icon" src="images/types/fairy.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Filled with pheromones, its poisonous gas can be diluted to use in the production of luscious perfumes.",
        footer: "Tier 3 • [75-120%] • No. 758 / Base Set 1",
        img: "https://i.imgur.com/IXoSe0J.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/salazzle.gif",
        type: 3,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  68   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  111   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Toxic Ash',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Higher PP</em><br><br><strong>5</strong>% 🍄 Poison Infliction<br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    33: {
        name: "Salandit (Fire)",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Volcanoes or dry, craggy places are its home. It emanates a sweet-smelling poisonous gas that attracts bug Pokémon, then attacks them.",
        footer: "Tier 2 • [55-100%] • No. 757 / Base Set 1",
        img: "https://i.imgur.com/tnc9uWZ.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/salandit.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  48   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  71   <strong>Def</strong>:  40"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Smolder',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.0</strong>  [+100%]<br><em>Increases with Higher PP</em><br><br><strong>5</strong>% 🍄 Poison Infliction<br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    34: {
        name: "Salazzle (Fire)",
        desc: '<img class="icon" src="images/types/fire.png">Fire Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/ice.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/water.png"><img class="icon" src="images/types/dragon.png">',
        bio: "Filled with pheromones, its poisonous gas can be diluted to use in the production of luscious perfumes.",
        footer: "Tier 3 • [75-120%] • No. 758 / Base Set 1",
        img: "https://i.imgur.com/nAz7aaz.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/salazzle.gif",
        type: 1,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  68   <strong>PP</strong>:  6   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  111   <strong>Def</strong>:  60"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Toxic Ash',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>1.12</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Higher PP</em><br><br><strong>5</strong>% 🍄 Poison Infliction<br><strong>5</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/nature.png"> Atk +<strong>1</strong>'
            }
        ]
    },
    14: {
        name: "Komala",
        desc: '<img class="icon" src="images/types/normal.png">Normal Type',
        bio: "The log it holds was given to it by its parents at birth. It has also been known to cling to the arm of a friendly Trainer.",
        footer: "Tier 2 • [55-100%] • No. 775 / Base Set 1",
        img: "https://i.imgur.com/XwMwvll.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/komala.gif",
        type: 0,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  65   <strong>PP</strong>:  4   <strong>Wt</strong>: Light<br><strong>Atk</strong>:  115   <strong>Def</strong>:  95"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Calm Mind',
                value: "<strong>2</strong> PP"
            },
            {
                name: '<span class="icon-num">1</span> Turn Buff',
                value: '<img class="icon" src="images/types/normal.png"> Atk +<strong>2</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: "💤 Sleep Talk<br><em>Can attack while sleeping.</em>"
            }
        ]
    },
    219: {
        name: "Turtonator",
        desc: '<img class="icon" src="images/types/dragon.png">Dragon Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fairy.png">',
        bio: "It gushes fire and poisonous gases from its nostrils. Its dung is an explosive substance and can be put to various uses.",
        footer: "Tier 3 • [75-120%] • No. 776 / Base Set 1",
        img: "https://i.imgur.com/tgCSfQS.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/turtonator.gif",
        type: 10,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  60   <strong>PP</strong>:  6   <strong>Wt</strong>: Heavy<br><strong>Atk</strong>:  91   <strong>Def</strong>:  135"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Dragon Mortar',
                value: "<strong>4</strong> PP 「Single Target」<br>Multi:  x<strong>0.91</strong> ~ <strong>1.4</strong><br>Z-Move:  x<strong>2.2</strong>  [+120%]<br><em>Increases with Later Slot</em><br><strong>Recoil!</strong> Lose <strong>10</strong>% of max HP<br>⏱ Recharge: <strong>1</strong> Turn<br><br><strong>15</strong>% 🔥 Burn Infliction"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/dragon.png"> Atk +<strong>1</strong><br><img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/dragon.png"> Enemy Def -<strong>1</strong>'
            }
        ]
    },
    72: {
        name: "Mimikyu (Psychic)",
        desc: '<img class="icon" src="images/types/psychic.png">Psychic Type<br><em>Strong Against:</em> <img class="icon" src="images/types/nature.png"><img class="icon" src="images/types/earth.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/psychic.png"><img class="icon" src="images/types/dark.png">',
        bio: "A lonely Pokémon, it conceals its terrifying appearance beneath an old rag so it can get closer to people and other Pokémon.",
        footer: "Tier 2 • [55-100%] • No. 778 / Base Set 1",
        img: "https://i.imgur.com/eAjxmR8.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/mimikyu.gif",
        type: 7,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  90   <strong>Def</strong>:  105"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Disguise',
                value: "<strong>2</strong> PP"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '2 Turn: <img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            }
        ]
    },
    73: {
        name: "Mimikyu (Fairy)",
        desc: '<img class="icon" src="images/types/fairy.png">Fairy Type<br><em>Strong Against:</em> <img class="icon" src="images/types/dark.png"><img class="icon" src="images/types/dragon.png"><br><em>Weak Against:</em> <img class="icon" src="images/types/fire.png"><img class="icon" src="images/types/fairy.png">',
        bio: "A lonely Pokémon, it conceals its terrifying appearance beneath an old rag so it can get closer to people and other Pokémon.",
        footer: "Tier 2 • [55-100%] • No. 778 / Base Set 1",
        img: "https://i.imgur.com/7wGh06B.png",
        thumb: "https://play.pokemonshowdown.com/sprites/xyani/mimikyu.gif",
        type: 8,
        fields: [{
                name: '<img class="icon" src="images/shield.png"> Stats',
                value: "<strong>HP</strong>:  55   <strong>PP</strong>:  6   <strong>Wt</strong>: Feather<br><strong>Atk</strong>:  90   <strong>Def</strong>:  105"
            },
            {
                name: '<img class="icon" src="images/sword.png"> Disguise',
                value: "<strong>2</strong> PP"
            },
            {
                name: '<span class="icon-num">2</span> Turn Buff',
                value: '<img class="icon" src="images/types/rainbow.png"> Def +<strong>1</strong>'
            },
            {
                name: '<img class="icon" src="images/sparkles.svg"> Passive',
                value: '2 Turn: <img class="icon" src="images/types/normal.png"> Def +<strong>1</strong><br><em>Blocks <strong>1</strong> move\'s damage entirely.</em>'
            }
        ]
    }
};


function sample(c, l, h) {
    var count = c,
        min = l,
        max = h,
        nums = {},
        out = [],
        r, len = 0;

    if (max - min < count) count = max - min;

    var getRand = function() {
            return Math.floor(Math.random() * (max - min) + min);
        },
        check = function(a) {
            return nums[a];
        },
        add = function(a) {
            nums[a] = 1;
            out.push(a);
            len++;
        };

    while (len < count) {
        if (len == 0) r = getRand();
        else
            while (check(r = getRand()));
        add(r);
    }
    return out;
}