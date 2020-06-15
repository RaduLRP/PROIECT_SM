var chart;
var data = new Array(20).fill(0);
var labels = data.map((val, index) => "o");

var THRESHOLD_CUTREMUR = 10;

function showAlarm(){
	document.getElementById("alarm").classList.remove("hidden");
}

function hideAlarm(){
	document.getElementById("alarm").classList.add("hidden");
}

function drawChart(){
	var ctx = document.getElementById("chart").getContext("2d");
	chart = new Chart(ctx, {
		type: "line",
		data: {
			labels: labels,
			datasets: [{
				label: "G's",
				backgroundColor: "rgb(255, 99, 132)",
				borderColor: "rgb(255, 99, 132)",
				data: data,
				fill: false
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: true,
						max: 30,
						min: 0,
						stepSize: 5
					}
				}]
			}
		}
	});
}

function updateChart(){
	chart.data.datasets[0].data = data;
	chart.update();
}

async function updateData(){
	var currentValue = 0;
	
	await new Promise((resolve) => {
		fetch("/getvalue").then(response => response.json()).then(data => {
			currentValue = data;
			resolve();
		});
	});
	
	if(currentValue > THRESHOLD_CUTREMUR){
		showAlarm();
		setTimeout(hideAlarm, 3000);
	}
	
	// scot primul element si pun altu' in coada
	data.shift();
	data.push(currentValue);
	
	updateChart();
	setTimeout(updateData, 200);
}

window.onload = function(){
	drawChart();
	setTimeout(updateData, 0);
}