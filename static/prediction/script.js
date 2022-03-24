const accident = document.querySelector("#accident-propability");
const noAccident = document.querySelector("#no-accident-propability");

accident.addEventListener('change', event => visualize());
noAccident.addEventListener('change', event => visualize());

const accidentPropability = parseFloat(accident.textContent);
const noAccidentPropability = parseFloat(noAccident.textContent);

const visualize = () => {
    console.log("Hello");
    if (isNaN(accidentPropability) || isNaN(noAccidentPropability)) {
        return;
    }
    
    const predictions = [
        {category: "Accident", "probability": accidentPropability},
        {category: "No accident", "probability": noAccidentPropability}
    ];
    
    const cf = crossfilter(predictions);
    const category = cf.dimension(p => p.category);
    
    dc.rowChart("#row-chart")
        .dimension(category)
        .group(category.group().reduceSum(p => p.value));
    
    dc.pieChart("#pie-chart")
        .dimension(category)
        .group(category.group().reduceSum(p => p.value));
    
    dc.renderAll();
};

window.onload = () => visualize();
document.onload = () => visualize();
