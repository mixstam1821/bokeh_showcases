# for more examples here my post here: https://discourse.bokeh.org/t/simple-interaction-with-echarts-js/12465
from bokeh.models import Slider, CustomJS, Paragraph
from bokeh.io import curdoc
from bokeh.layouts import column

# ─── UI ELEMENTS ──────────────────────────────────────────────
text_area = Paragraph(text='🌍 Interactive 3D Globe with Auto-Rotate')

slider = Slider(
    start=1,
    end=20,
    value=5,
    step=1,
    title="Rotation Speed"
)

# ─── JAVASCRIPT CALLBACK ──────────────────────────────────────
sphere_js = CustomJS(args=dict(slider=slider), code="""
(function() {
    function createGlobe() {
        if (typeof echarts === 'undefined') {
            const script1 = document.createElement('script');
            script1.src = 'https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js';
            script1.onload = function() {
                const script2 = document.createElement('script');
                script2.src = 'https://cdn.jsdelivr.net/npm/echarts-gl@2.0.9/dist/echarts-gl.min.js';
                script2.onload = renderGlobe;
                document.head.appendChild(script2);
            };
            document.head.appendChild(script1);
        } else {
            renderGlobe();
        }
    }

    function renderGlobe() {
        let chartEl = document.getElementById("echarts_sphere_canvas");
        if (!chartEl) {
            chartEl = document.createElement("div");
            chartEl.id = "echarts_sphere_canvas";
            chartEl.style.cssText = `
                position: fixed;
                top: 80px;
                left: 50%;
                transform: translateX(-50%);
                width: 700px;
                height: 500px;
                z-index: 10;
                background-color: black;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0,255,255,0.2);
            `;
            document.body.appendChild(chartEl);
        }

        const myChart = echarts.init(chartEl);
        const speed = slider.value;

        const option = {
            backgroundColor: '#000',
            globe: {
                baseTexture: 'https://cdn.jsdelivr.net/gh/apache/echarts-website@asf-site/examples/data-gl/asset/world.topo.bathy.200401.jpg',
                heightTexture: 'https://cdn.jsdelivr.net/gh/apache/echarts-website@asf-site/examples/data-gl/asset/bathymetry_bw_composite_4k.jpg',
                shading: 'realistic',
                environment: '#000',
                realisticMaterial: {
                    roughness: 0.8,
                    metalness: 0
                },
                viewControl: {
                    autoRotate: true,
                    autoRotateSpeed: speed,
                    distance: 160
                },
                light: {
                    main: { intensity: 1.2 },
                    ambient: { intensity: 0.3 }
                }
            }
        };

        myChart.setOption(option);
        window.addEventListener("resize", () => myChart.resize());
    }

    // Delay to allow DOM readiness
    setTimeout(createGlobe, 100);
})();
""")

# ─── EVENT BINDING ────────────────────────────────────────────
slider.js_on_change('value', sphere_js)
curdoc().js_on_event('document_ready', sphere_js)

# ─── APP ROOT ─────────────────────────────────────────────────
curdoc().add_root(column(text_area, slider))
