

var fillColors = {'0': '#FFFFAA',
        '1': '#DDFFAA',
        '2': '#BBFFAA',
        '3': '#99FFAA',
        '4': '#77FFAA',
        '5': '#55FFAA',
        '6': '#33FFAA',
        '7': '#11FFAA',
        '8': '#00FFAA',
        defaultFill: '#FFFFDD'
        };

function showSelected(e) {
    var target = e.target || e.srcElement;
    //rect3text.firstChild.data = data[target.id]["description"];
    //document.getElementById("stateDescription").innerHTML = data[target.id]["description"];
    //rect3.style.fill = target.style.fill
    //target.style.fill = "#EEEEEE";
    target.style.opacity = .5;
    target.style.stroke = "#000000"
    m.appendChild(target);
};

function selectState(e) {
    var target = e.target || e.srcElement;
    document.getElementById("stateDescription").innerHTML = data[target.id]["description"];
};

function unselect(e) {
    var target = e.target || e.srcElement;
    target.style.opacity = 1.;
    target.style.stroke = fillColors[data[target.id]["fillKey"]]
    //document.getElementById("stateDescription").innerHTML = "";
};

var m = document.getElementById("map");
var states = m.getElementsByClassName("state");

for (var i = 0; i < states.length; i++) {
    //states[i].style.fill = "#333300";
    states[i].style.fill = fillColors[data[states[i].id]["fillKey"]];
    states[i].style.stroke = fillColors[data[states[i].id]["fillKey"]];
    states[i].style["stroke-width"] = "2";
    states[i].onmouseover = showSelected;
    states[i].onmouseout = unselect;
    states[i].onclick = selectState;
    };

var m = document.getElementById("map");
var legendBoxes = m.getElementsByClassName("legendBox");
for (var i = 0; i < legendBoxes.length; i++) {
    legendBoxes[i].style.fill = fillColors[i];
    legendBoxes[i].style.stroke = fillColors[i];
    legendBoxes[i].style["stroke-width"] = "2";
    //legendBoxes[i].onmouseover = ;
    //legendBoxes[i].onmouseout = ;
    };
