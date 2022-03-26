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
        data: info.fpr.map((_fpr, index) => {
            return {
                x: _fpr,
                y: info.tpr[index]
            };
        }),
        showLine: true
    };
});

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

const data = {
    datasets: _datasets
};

// ===== Options =====

const options = {
    plugins: {
        title: {
            display: true,
            text: 'ROC Curves'
        }
    },
    // Doesn't work
    legend: {
        labels: {
            filter: (legendItem, data) => legendItem.text !== 'No-skill'
        }
    },
};

// ===== Config =====

const config = {
    type: 'scatter',
    data: data,
    options: options
};

// ===== Chart =====

const myChart = new Chart(
    document.getElementById('chart'),
    config
);
