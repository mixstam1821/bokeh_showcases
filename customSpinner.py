# https://discourse.bokeh.org/t/custom-spin-loader/12469
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button, Div
from bokeh.plotting import figure
import time

# ─── FAKE JOB STATUS FUNCTION ─────────────────────────────────
def is_job_done():
    """
    Simulates a backend job status check.
    Replace this with real async data fetch or status polling.
    """
    time.sleep(2)  # Simulate backend delay
    return 1

# ─── LOADING SPINNER HTML ─────────────────────────────────────
wait_html = """
<div class="spin-wrapper">
  <img src="https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/2784386.png" class="spinner-img">
  <p class="loader-msg">⏳ Loading... Stand by.</p>
</div>

<style>
.spin-wrapper {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.spinner-img {
  width: 120px;
  height: 120px;
  animation: spin-fast 1.4s linear infinite;
  filter: drop-shadow(0 0 6px #1a73e8);
}
@keyframes spin-fast {
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.loader-msg {
  margin-top: 16px;
  font-size: 18px;
  color: #ccc;
  font-family: 'Segoe UI', sans-serif;
}
</style>
"""

# ─── UI COMPONENTS ────────────────────────────────────────────
div = Div(text="", width=600, height=320)

# Define 4 sample plots (you can customize titles/data as needed)
plots = []
for i in range(4):
    p = figure(height=250, width=600, title=f"📊 Plot {i+1}")
    p.line([1, 2, 3, 4], [4-i, 2+i, 3, 1], line_width=3, color="#1a73e8")
    p.visible = False
    plots.append(p)

# ─── BUTTON ───────────────────────────────────────────────────
button = Button(label="▶️ Start Simulation", button_type="success", width=260)

# ─── JOB POLLING LOGIC ────────────────────────────────────────
def poll_job_status():
    if is_job_done() == 1:
        for p in plots:
            p.visible = True
        layout.children[1] = column(row(plots[0],plots[1]),row(plots[2],plots[3]))  # replace spinner with all plots
    else:
        curdoc().add_timeout_callback(poll_job_status, 1)

# ─── BUTTON CLICK CALLBACK ────────────────────────────────────
def on_click():
    div.text = wait_html
    layout.children[1] = div
    for p in plots:
        p.visible = False
    curdoc().add_timeout_callback(poll_job_status, 1)

button.on_click(on_click)

# ─── FINAL LAYOUT ─────────────────────────────────────────────
layout = column(button, div)
curdoc().add_root(layout)
