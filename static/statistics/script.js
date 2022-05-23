// === Scatter charts ===

const allLabelsFilter = (legendItem, data) => {return !isROC || legendItem.text !== 'No-skill';}

const drawCurves = (queryString, title, x_dataKey, y_dataKey, isROC = false) => {
    // ===== Data =====

    const _datasets = backbone_info.map((info, index) => {
        const r = Math.random() * 255;
        const g = Math.random() * 255;
        const b = Math.random() * 255;
        const color = `rgb(${r}, ${g}, ${b})`;

        return {
            label: info.name,
            radius: 1,
            pointHoverRadius: 8,
            backgroundColor: color,
            borderColor: color,
            data: info[x_dataKey].map((x, index) => {
                return {
                    x: x,
                    y: info[y_dataKey][index]
                };
            }),
            showLine: true
        };
    });

    if (isROC) {
        _datasets.push({
            label: 'No-skill',
            backgroundColor: 'rgb(60, 60, 60)',
            borderColor: 'rgb(60, 60, 60)',
            data: [{
                x: 0,
                y: 0
            }, {
                x: 1,
                y: 1
            }],
            showLine: true,
            borderDash: [10,10]
        });
    }

    const data = {
        datasets: _datasets
    };

    // ===== Options =====

    const options = {
        plugins: {
            title: {
                display: true,
                text: title
            },
            legend: {
                labels: {
                    filter: allLabelsFilter
                },
                onClick: null
            }
        }
    };

    // ===== Config =====

    const config = {
        type: 'scatter',
        data: data,
        options: options
    };

    // ===== Chart =====

    return new Chart(
        document.querySelector(queryString),
        config
    );
};


// === Bar charts ===

const drawBarChart = () => {    
    
    const borderColor = backbone_info.map((info, index) => {
        const r = Math.random() * 255;
        const g = Math.random() * 255;
        const b = Math.random() * 255;
        
        return `rgba(${r}, ${g}, ${b}, 1)`;
    });

    const backgroundColor = borderColor.map((rgbaStr) => {
        const rgbaList = rgbaStr.split(", ");
        rgbaList[rgbaList.length - 1] = '0.2)'; // alpha value
    
        return rgbaList.join(", ");
    });

    const _data = backbone_info.map((info, index) => {
        return {
            label: info.name,
            backgroundColor: [backgroundColor[index]],
            borderColor: [borderColor[index]],
            data: [info['auc']],
            borderWidth: 1
        };
    });
    
    console.log(_data)
    const data = {
        labels: ['AUC'],
        datasets: _data
    };
    
    
    const options = {
        plugins: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            title: {
                display: true,
                text: "AUC Scores"
            },
            legend: {
                labels: {
                    filter: allLabelsFilter
                },
                onClick: null // disable filter on legend touched, cuz this causes bug
            }
        }
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: options,
    };
    
    return new Chart(
        document.querySelector("#AUC-chart"),
        config
    );
}

const ROCChart = drawCurves(queryString = '#ROC-chart', title = "ROC Curves", x_dataKey = "fpr", y_dataKey = "tpr", isROC = true);
const AUCBarChart = drawBarChart()

// === Chart filter ===

const chartFilter = (filter) => {
    for (const chart of [ROCChart, AUCBarChart]) {
        for (let i = 0; i < backbone_info.length; i++) {
            // chart.getDatasetMeta(i).hidden = backbone_info[i].name !== filter;
            if (filter === 'all') {
                chart.options.plugins.legend.labels.filter = allLabelsFilter;
                chart.data.datasets[i].hidden = false;
            }
            else {
                chart.data.datasets[i].hidden = backbone_info[i].name !== filter;
                chart.options.plugins.legend.labels.filter = (legendItem, data) => { return legendItem.text === filter; };                
            }
            chart.update();
        }
    }
};

for (const info of backbone_info) {
    let name = info.name.replace(/ /g,'').toLowerCase();
    let idName = "v-pills-" + name + "-tab";
    document.getElementById(idName).addEventListener("click", () => { chartFilter(info.name); dropdown(info.name); });    
}
document.getElementById("v-pills-all-tab").addEventListener("click", () => { chartFilter('all'); dropdown('All'); });    

function dropdown(val) {
    var y = document.getElementsByClassName('btn btn-secondary dropdown-toggle');
    var aNode = y[0].innerHTML = val; // Append

    // === Confusion matrix ===

    const CM_PATH = "/static/visualization/";
    let cmFile = "";
    switch (val) {
        case "Mobile-Net+Conv3D": cmFile = "mobilenet+conv3d_cm.PNG"; break;
        case "Mobile-Net+ConvLSTM": cmFile = "mobilenet+convlstm_cm.PNG"; break;
        case "Mobile-Net+Bi-ConvLSTM": cmFile = "mobilenet+biconvlstm_cm.PNG"; break;
        case "Mobile-Net+TAConv3D": cmFile = "mobilenet+taconv3d_cm.PNG"; break;
        case "Dense-Net121+Conv3D": cmFile = "densenet+conv3d_cm.PNG"; break;
        case "Dense-Net121+Bi-ConvLSTM": cmFile = "densenet+biconvlstm_cm.PNG"; break;
        case "Inceptionv3+Conv3D": cmFile = "inception+conv3d_cm.PNG"; break;
        case "Inceptionv3+ConvLSTM": cmFile = "inception+convlstm_cm.PNG"; break;
        case "Res-Net 152v2": cmFile = "resnet_cm.PNG"; break;
        case "VGG16": cmFile = "vgg16_cm.PNG"; break;
        case "Res-Net+CBAM+ConvLSTM": cmFile = "res-net+cbam+convlstm_cm.PNG"; break;
        case "Res-Net+SE+ConvLSTM": cmFile = "res-net+se+convlstm_cm.png"; break;
    }
    cmFile = CM_PATH + cmFile;

    const cm = document.getElementById('cm');
    cm.style.backgroundImage = "url('" + cmFile + "')";
}
