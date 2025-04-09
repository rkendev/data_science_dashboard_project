from fasthtml.common import FastHTML, H1, Div, serve
import matplotlib.pyplot as plt
# Import submodules within report
from .utils import load_model
from .base_components import Dropdown, BaseComponent, Radio, MatplotlibViz, DataTable
from .combined_components import FormGroup, CombinedComponent
from employee_events.employee import Employee
from employee_events.team import Team

# ReportDropdown
class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model):
        self.label = model.name
        self.value = str(entity_id)
        self.model = model  # Save the model for rendering
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):
        data = []
        for text, numeric_id in model.names():
            data.append((text, str(numeric_id)))
        return data

    def render(self):
        data = self.component_data(self.value, self.model)
        html = f'<label for="{self.id}">{self.label.lower()}</label>'
        html += f'<select name="{self.name}" id="{self.id}">'
        for text, option_value in data:
            selected_attr = ' selected' if option_value == self.value else ''
            html += f'<option value="{option_value}"{selected_attr}>{text}</option>'
        html += '</select>'
        return html

class Header(BaseComponent):
    def build_component(self, entity_id, model):
        return H1(f"{model.name.capitalize()} Dashboard")

class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model):
        df = model.event_counts(entity_id).fillna(0)
        df = df.set_index("event_date").sort_index()
        df[["positive_events", "negative_events"]] = df[
            ["positive_events", "negative_events"]
        ].cumsum()
        df.columns = ["Positive", "Negative"]
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        ax.set_title("Cumulative Positive/Negative Events Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        return fig

class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model):
        df = model.model_data(entity_id)
        pred_probs = self.predictor.predict_proba(df)
        p = pred_probs[:, 1]
        pred = p.mean() if model.name == "team" else (p[0] if p.size else 0)
        fig, ax = plt.subplots()
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        return fig

class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls="grid")

class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)

# Modified DashboardFilters with attributes added to the Radio element
class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(values=["Employee", "Team"], name="profile_type"),
        ReportDropdown(id="selector", name="user-selection"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Attach the HTMX attributes to the Radio element
        radio = self.children[0]
        radio.attrs = {
            "hx-get": "/update_dropdown",
            "hx-target": "#selector",
            "hx-trigger": "change delay:500ms",
            "hx-params": "*",
        }

class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]

app = FastHTML(__name__)
report_page = Report()

@app.get("/")
def index():
    return report_page(1, Employee())

@app.get("/employee/{id}")
def employee_page(id: int):
    return report_page(id, Employee())

@app.get("/team/{id}")
def team_page(id: int):
    return report_page(id, Team())

@app.get("/update_dropdown{r}")
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    prof_type = r.query_params.get("profile_type")
    selected_id = r.query_params.get("user-selection", "1")
    print("PARAM", prof_type, "ID", selected_id)
    if prof_type == "Team":
        return dropdown(selected_id, Team())
    elif prof_type == "Employee":
        return dropdown(selected_id, Employee())

@app.post("/update_data")
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict["profile_type"]
    asset_id = data._dict["user-selection"]
    if profile_type == "Employee":
        return RedirectResponse(f"/employee/{asset_id}", status_code=303)
    elif profile_type == "Team":
        return RedirectResponse(f"/team/{asset_id}", status_code=303)

serve()