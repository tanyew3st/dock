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
let mlarray

// time it takes between structures
let interval1
let interval
let esttime

var namesArray = {
    "knn": "K Nearest Neighbor",
    "lr": "Logistic Regression",
    "svm": "Support Vector Machines",
    "rf": "Random Forest"
}

function makeGraph() {

    var ctx = document.getElementById("myChart").getContext("2d");
    map = this.mlarray
    var data = {}

    let datasets = []
    let labels = []

    let percActive = {
        label: "% Chance Active",
        fill: true,
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(30, 144, 255 , 1)",
        borderWidth: 2,
        data: new Array()
    }

    let percDecoy = {
        label: "% Chance Decoy",
        fill: true,
        backgroundColor: "rgba(255,99,132,0.2)",
        borderColor: "rgba(255,99,132,1)",
        borderWidth: 2,
        data: new Array()

    }

    for (let key in map) {

        labels.push(this.namesArray[key])
        percActive.data.push(map[key][0].toString().substring(0, 7))
        percDecoy.data.push(map[key][1].toString().substring(0, 7))
    }

    var data = {
        labels: labels,
        datasets: [percActive, percDecoy]
    };
    
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            barValueSpacing: 20,
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,
                    }
                }]
            }
        }
    });
    
}

function pdf() {
    html2canvas(document.getElementById("frame"),
        {
        onrendered:function(canvas) {
            let a = document.createElement("a")
            a.href = canvas.toDataURL("image/png")
            a.download = "image.png"
            a.click()
        }
    })
}

// getting the structure names
function func1(ligand, protein) {
    document.getElementById("reassurance").style.display = "block"
    document.getElementById("showprogress").style.display = "block"
    var url = window.location.href
    base = url.substr(0, url.indexOf('/run'));
    var o = {
        "bod": "hello world"
    }
    this.protein = protein
    this.ligand = ligand

    // getting from the server
    fetch(base + '/structures/get/' + protein)
        .then(response => response.json())
        .then(json => {
            finished = false
            currentstr = 0
            structures = json.sort()
            max = structures.length
            interval = parseFloat(((1/max) * 100).toString().substring(0,5))

            createTable(structures)
            affinity = new Map()
            getAffinity()
        })
}

function getAffinity() {
        // document.getElementById(structures[currentstr]).innerHTML = "..."
        document.getElementById(structures[currentstr]).classList.add("loading")

        initialTime = performance.now()
        if (structures[currentstr] == ".DS_Store") {
            currentstr++
        }
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
            document.getElementById(structures[currentstr]).classList.remove("loading")
            updateTable(currentstr, res['affinity'])
            this.affinity.set(structures[currentstr], res['affinity'])
            currentstr++
            if (currentstr === max) {
                finished = true
                clearInterval(interval1)
                if (localStorage.getItem("option") == "mldocking") {
                    console.log(this.affinity)
                    machineLearn()
                } else {
                    alert("everything is finished rn")
                }
            } else {
                clearInterval(interval1)
                document.getElementById("progress").innerHTML = (100 *((currentstr) / max)).toString().substring(0, 5) + "%"
                document.getElementById("progress").style.width = (100 * ((currentstr) / max)) + "%"
                console.log(this.affinity)
                let time = (performance.now() - initialTime) / 1000
                interval1 = setInterval(function() {
                    let currentTime = document.getElementById("progress").innerHTML
                    currentTime = currentTime.substring(0, currentTime.length - 1);
                    currentTime = parseFloat(currentTime)
                    let newTime = currentTime + (((5/time)*interval))
                    document.getElementById("progress").innerHTML = (newTime + "%").toString().substring(0, 5)
                    document.getElementById("progress").style.width = newTime + "%"
                    let esttime = (max * time) * (1 - newTime / 100)
                    console.log(esttime)
                    console.log((max * time))
                    console.log((1 - newTime / 100))
                    console.log((max * time) * (1 - newTime / 100))
                    let seconds = Math.round(esttime % 60)
                    if (seconds < 10) {
                        seconds = "0" + seconds.toString()
                    }
                    document.getElementById("time").innerHTML = Math.floor(esttime/60) + ":" + seconds
                }, 5000)
                getAffinity()
            }

        })
        console.log(obj)
}

function createTable(names) {
    console.log(names)
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

function machinelearning() {
    console.log(this.affinity)
    console.log("Machine learning");
    if (this.protein === undefined) {
        this.protein = localStorage.getItem("protein")
    }

    console.log("uhhh...")
    let linear = localStorage.getItem("linear")
    console.log(JSON.stringify({"affinity": this.affinity, "protein": this.protein, "linear": linear}))
    fetch(base + '/run/ml/array', {
        method: "POST",
        body: JSON.stringify({"affinity": this.affinity, "protein": this.protein, "linear": linear})
    }).then(response => response.json())
    .then(res => {
        document.getElementById("alert").classList.replace("alert-danger", "alert-success")
        document.getElementById("alert").innerHTML = "Success - Data Displayed Below!"
        setTimeout(function() {
            document.getElementById("alert").remove()
        }, 5000)
        this.mlarray = res
        makeGraph()
        makeMLTable()
    })
}

function makeMLTable() {
    console.log(this.mlarray)
    for (let [key, value] of Object.entries(this.mlarray)) {
        console.log(key)
        console.log(value[0])

        let row = document.createElement("tr");
        row.id = "tableRow"

        let el = document.createElement("th")
        el.innerHTML = this.namesArray[key]
        row.appendChild(el)

        let tw = document.createElement("td")
        tw.innerHTML = value[0].toString().substring(0,7)
        row.appendChild(tw)
    
        let tw2 = document.createElement("td")
        tw2.innerHTML = value[1].toString().substring(0,7)
        row.appendChild(tw2)

        document.getElementById("mlBody").appendChild(row)
    }
}

function getSampleScores(type, protein) {
    document.getElementById('submit2').setAttribute('disabled', 'disabled');
    document.getElementById('submit5').setAttribute('disabled', 'disabled');
    document.getElementById('submit6').setAttribute('disabled', 'disabled');
    document.getElementById('protein2').setAttribute('disabled', 'disabled');
    fetch('/sample/' + protein + '/' + type)
        .then(response => response.json())
        .then(json => {
            console.log(json)
            getStructures(protein)
            document.getElementById("textarea").value = JSON.stringify(json)

        })
}


function getStructures(protein) {
    document.getElementById('submit2').setAttribute('disabled', 'disabled');
    document.getElementById('protein2').setAttribute('disabled', 'disabled');
    document.getElementById('submit5').setAttribute('disabled', 'disabled');
    document.getElementById('submit6').setAttribute('disabled', 'disabled');
    document.getElementById("textarea").removeAttribute('disabled')
    document.getElementById('submit3').removeAttribute('disabled')
    document.getElementById('submit4').removeAttribute('disabled')
    console.log('printing...')
    let url = window.location.href
    base = url.substr(0, url.indexOf('/run'));
    this.base = base

    fetch(base + '/structures/get/' + protein)
    .then(response => response.json())
    .then(json => {
        localStorage.setItem("protein", protein)
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

function submitAffinity(val, linear) {
    localStorage.setItem("affinity", JSON.stringify(val))
    localStorage.setItem("linear", linear)
    window.location.href = "/results"
}

function setLinear(linear) {
    localStorage.setItem("linear", linear)
}
function machineLearn() {
    document.getElementById("alert").style.display = "block"
    if (this.affinity === undefined) {
        this.affinity = JSON.parse(JSON.parse(localStorage.getItem("affinity")))
        var url = window.location.href
        base = url.substr(0, url.indexOf('/results'));

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

        machinelearning()
    } else {
        console.log(this.affinity)
        var url = window.location.href
        base = url.substr(0, url.indexOf('/'));

        // let unordered = this.affinity
        // const ordered = {};
        // Object.keys(unordered).sort().forEach(function(key) {
        //   ordered[key] = unordered[key];
        // });
        //
        // this.affinity = ordered

        this.structures = Object.keys(this.affinity)
        console.log(this.affinity)
        machinelearning()
    }
}