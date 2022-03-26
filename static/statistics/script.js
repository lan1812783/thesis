
const drawCurves = (queryString, title, x_dataKey, y_dataKey, isROC = false) => {
    // ===== Data =====

    const _datasets = backbone_info.map((info, index) => {
        const r = Math.random() * 255;
        const g = Math.random() * 255;
        const b = Math.random() * 255;
        const color = `rgb(${r}, ${g}, ${b})`;

        return {
            label: info.name,
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
                    filter: (legendItem, data) => !isROC || legendItem.text !== 'No-skill'
                }
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

    const chart = new Chart(
        document.querySelector(queryString),
        config
    );
    console.log(chart.data)
}

drawCurves(queryString = '#ROC-chart', title = "ROC Curves", x_dataKey = "fpr", y_dataKey = "tpr", isROC = true);
drawCurves(queryString = '#model-train-accuracy-chart', title = "Model train accuracy", x_dataKey = "epochs", y_dataKey = "model_train_accuracy");
drawCurves(queryString = '#model_val_accuracy', title = "Model validation accuracy", x_dataKey = "epochs", y_dataKey = "model_val_accuracy");
drawCurves(queryString = '#model_train_loss', title = "Model train loss", x_dataKey = "epochs", y_dataKey = "model_train_loss");
drawCurves(queryString = '#model_val_loss', title = "Model validation loss", x_dataKey = "epochs", y_dataKey = "model_val_loss");
