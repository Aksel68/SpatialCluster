$main

const MAX_RADIUS = $radio;

// A linear scale to position the nodes on the X axis
let x = d3.scalePoint()
    .range([0, widthSVG])
    .domain(dataset.nodes.map((d) => d.id))

let idToNode = {};
dataset.nodes.forEach(function(n) {
    idToNode[n.id] = n;
});

let links = container
    .selectAll('path')
    .data(dataset.links)
    .enter()
    .append('path')
    .attr('d', function(d) {
        start = x(idToNode[d.source].id) // X position of start node on the X axis
        end = x(idToNode[d.target].id) // X position of end node
        return ['M', start, heightSVG - MAX_RADIUS, // the arc starts at the coordinate x=start, y=heightSVG-30 (where the starting node is)
                'A', // This means we're gonna build an elliptical arc
                (start - end) / 2, ',', // Radius in X
                Math.min(Math.abs(start - end) / 2, heightSVG), // Radius in Y
                0, 0, ',',
                start < end ? 1 : 0, end, ',', heightSVG - MAX_RADIUS
            ] // We always want the arc on top. So if end is before start, putting 0 here turn the arc upside down.
            .join(' ');
    })

let nodes = container
    .selectAll("circle")
    .data(dataset.nodes)
    .enter()
    .append("circle")
    .attr("cx", function(d) { return (x(d.id)) })
    .attr("cy", heightSVG - MAX_RADIUS)
    .attr("r", MAX_RADIUS)

nodes
    .on('mouseover', function(_, d) {
        nodes.style('fill', "#B8B8B8")
        links
            .style('stroke', (link_d) => link_d.source === d.id || link_d.target === d.id ? '#69b3b2' : '#b8b8b8')
            .style('stroke-width', (link_d) => link_d.source === d.id || link_d.target === d.id ? 2 : 0.3)
    })
    .on('mouseout', function(d) {
        nodes.style('fill', "#69b3a2")
        links
            .style('stroke', 'black')
            .style('stroke-width', 0.3)
    })