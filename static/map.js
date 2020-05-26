var max = 0
var finished = false
var currentstr = 0
var structures
var protein
var ligand
var base
var max
var affinity
let initialTime

// time it takes between structures
let interval1
let interval
let esttime

let something = "hello"

function printSomething() {
    console.log(something)
    something = something + something
}
// getting the structure names
function func1(ligand, protein) {
    var url = window.location.href
    console.log(interval);
    base = url.substr(0, url.indexOf('/run'));
    console.log(base);
    var o = {
        "bod": "hello world"
    }
    this.protein = protein
    this.ligand = ligand

    // getting from the server
    fetch(base + '/structures/get/' + protein)
        .then(response => response.json())
        .then(json => {
            console.log(json)
            finished = false
            currentstr = 0
            structures = json
            max = structures.length
            interval = parseFloat(((1/max) * 100).toString().substring(0,5))

            createTable(structures)
            affinity = new Map()
            getAffinity()
        })
}

function getAffinity() {
        document.getElementById(structures[currentstr]).innerHTML = "..."
        initialTime = performance.now()
        if (structures[currentstr] == ".DS_Store") {
            currentstr++
        }
        console.log("working... testing structure " + structures[currentstr])
        // need to dock every structure with every protein
        let obj = {
            "protein": protein,
            "structure": structures[currentstr],
            "ligand": ligand
        }
        fetch(base + '/dock', {
            method: "POST",
            body: JSON.stringify(obj)
        }).then(response => response.json())
        .then(res => {
            console.log(this.affinity)
            console.log(res)
            updateTable(currentstr, res['affinity'])
            this.affinity.set(structures[currentstr], res['affinity'])
            currentstr++
            if (currentstr === max) {
                finished = true
                console.log(this.affinity)
            } else {
                clearInterval(interval1)
                console.log(this.affinity)
                let time = performance.now() - initialTime
                interval1 = setInterval(function() {
                    let currentTime = document.getElementById("progress").innerHTML
                    currentTime = currentTime.substring(0, currentTime.length - 1);
                    currentTime = parseFloat(currentTime)
                    document.getElementById("progress").innerHTML = currentTime + (((5000/time)*interval)) + "%"
                    document.getElementById("progress").style.width = currentTime + (((5000/time)*interval)) + "%"
                    let esttime = (max * time) * (1 - (currentTime + ((5000/time)*interval))/100)
                    document.getElementById("time").innerHTML = esttime
                }, 5000)
                console.log("took " + time + " seconds?");
                getAffinity()
            }

        })
        console.log(obj)
}

function createTable(names) {
    document.getElementById("progress").style.width = '1%'
    document.getElementById("progress").innerHTML = '1%'
    for (let i = 0; i < names.length; i++) {
        let el = document.createElement("th");
        el.innerHTML = names[i]
        document.getElementById("structures").appendChild(el)

        let tw = document.createElement("td")
        tw.id = names[i]
        document.getElementById("affinities").appendChild(tw)
    }

    console.log(document.getElementById("strtable"));
}

function updateTable(structureInput, num) {
    document.getElementById(structures[structureInput]).innerHTML = num
    structureInput += 1
    document.getElementById("progress").style.width = ((structureInput/max)*100).toString().substring(0,5) + "%"
    document.getElementById("progress").innerHTML = ((structureInput/max)*100).toString().substring(0,5) + "%"
    this.percentage = ((structureInput/max)*100).toString().substring(0,5)
}

function machinelearning(array) {
    fetch(base + '/run/ml/array', {
        method: "POST",
        body: JSON.stringify({"affinity": this.affinity})
    }).then(response => response.json())
    .then(res => {
        console.log(res)
    })
}

$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});


function getStructures(protein) {
    console.log('printing...')
    let url = window.location.href
    base = url.substr(0, url.indexOf('/run'));
    fetch(base + '/structures/get/' + protein)
    .then(response => response.json())
    .then(json => {
        console.log(json)
        for (structure of json) {
            if (structure !== ".DS_Store") {
                let divel = document.createElement("div")
                let inputel = document.createElement("input")
                let labelel = document.createElement("label")
                labelel.innerHTML = structure
                inputel.id = structure
                inputel.type = "text"
                inputel.className = "form-control"
                inputel.type = "number"
                inputel.max = 0
                inputel.min = -20
                divel.style.width = "6rem"
                divel.style.margin = "1rem"
                divel.appendChild(labelel)
                divel.appendChild(inputel)
                document.getElementById("smalltextbox").appendChild(divel)
                console.log(document.getElementById("smalltextbox"))
            }
        }

    })
}

function submitAffinity(val) {
    localStorage.setItem("affinity", JSON.stringify(val))
    window.location.href = "/results"
    // this.affinity = (localStorage.getItem("affinity"));
    // let hi = (JSON.parse(affinity))
    // let hiagain = JSON.parse(hi)
    // console.log(hiagain);
    // fetch(base + '/ml/render/page', {
    //         method: "POST",
    //         body: JSON.stringify(obj)})
    // .then(response => response.json())
    // .then(json => {
    //     console.log(json)
    // })
}

function machineLearn() {
    console.log(this.affinity)
    if (this.affinity === undefined) {
        this.affinity = JSON.parse(JSON.parse(localStorage.getItem("affinity")))

        let unordered = this.affinity
        const ordered = {};
        Object.keys(unordered).sort().forEach(function(key) {
          ordered[key] = unordered[key];
        });
        this.affinity = ordered

        this.structures = Object.keys(this.affinity)

        this.createTable(this.structures)
        for (let i in this.affinity) {
            document.getElementById(i).innerHTML = this.affinity[i]
        }
        document.getElementById("progress").style.width = "100%"
        document.getElementById("progress").innerHTML = "100%"
    }
}