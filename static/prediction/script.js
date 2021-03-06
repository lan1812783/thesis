const accident = document.querySelector("#accident-propability");
const noAccident = document.querySelector("#no-accident-propability");

const accidentPropability = parseFloat(accident.textContent);
const noAccidentPropability = parseFloat(noAccident.textContent);

const visualize = () => {
    if (isNaN(accidentPropability) || isNaN(noAccidentPropability)) {
        return;
    }
    
    const predictions = [
        {category: "Accident", probability: accidentPropability},
        {category: "No accident", probability: noAccidentPropability}
    ];
    
    const cf = crossfilter(predictions);
    const category = cf.dimension(p => p.category);
    
    dc.rowChart("#row-chart")
        .dimension(category)
        .group(category.group().reduceSum(p => p.probability));
    
    dc.pieChart("#pie-chart")
        .dimension(category)
        .group(category.group().reduceSum(p => p.probability));
    
    dc.renderAll();
};

visualize();
