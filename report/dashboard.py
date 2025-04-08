from fasthtml.common import *
import matplotlib.pyplot as plt


# import from submodules WITHIN report
from .utils import load_model
from .base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)


from .combined_components import FormGroup, CombinedComponent
from employee_events.query_base import QueryBase
from employee_events.employee import Employee
from employee_events.team import Team


# ReportDropdown
class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model):
        """
        Overwrites parent build_component(entity_id, model).
        Sets self.label to model.name, then sets self.value to str(entity_id).
        """
        self.label = model.name  
        self.value = str(entity_id)  # So the dropdown "remembers" the selected item
        return super().build_component(entity_id, model)


    def component_data(self, entity_id, model):
        """
        Returns a list of (display_text, string_id) so the dropdown can match self.value.
        """
        data = []
        for (text, numeric_id) in model.names():
            data.append((text, str(numeric_id)))  # e.g. ("Alex Martinez", "1")
        return data


class Header(BaseComponent):
    def build_component(self, entity_id, model):
        return H1(f"{model.name.capitalize()} Dashboard")


class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model):
        df = model.event_counts(entity_id).fillna(0)
        df = df.set_index('event_date').sort_index()
        df[['positive_events', 'negative_events']] = df[['positive_events','negative_events']].cumsum()
        df.columns = ['Positive', 'Negative']
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        ax.set_title('Cumulative Positive/Negative Events Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')
        return fig


class BarChart(MatplotlibViz):
    predictor = load_model()
    def visualization(self, entity_id, model):
        df = model.model_data(entity_id)
        pred_probs = self.predictor.predict_proba(df)
        p = pred_probs[:, 1]
        if model.name == "team":
            pred = p.mean()
        else:
            pred = p[0] if len(p) else 0

        fig, ax = plt.subplots()
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        return fig


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')


class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"


    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector',
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]


class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


app = FastHTML(__name__)
report_page = Report()


@app.get("/")
def index():
    """Default route => employee_id=1 dashboard."""
    return report_page(1, Employee())


@app.get("/employee/{id}")
def employee_page(id: int):
    """Displays the page for a given employee ID."""
    return report_page(id, Employee())

@app.get("/team/{id}")
def team_page(id: int):
    """Displays the page for a given team ID."""
    return report_page(id, Team())


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    """
    Called when user switches from 'Employee' to 'Team' or vice versa.
    We parse the last 'user-selection' from query params if available,
    so the dropdown can remain on the same ID or default to '1' if missing.
    """
    dropdown = DashboardFilters.children[1]
    prof_type = r.query_params.get('profile_type')  # "Team" or "Employee"
    # Try to get the user-selection param
    selected_id = r.query_params.get('user-selection', '1')  # default to "1"
    print('PARAM', prof_type, 'ID', selected_id)

    if prof_type == 'Team':
        return dropdown(selected_id, Team())
    elif prof_type == 'Employee':
        return dropdown(selected_id, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    asset_id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{asset_id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{asset_id}", status_code=303)


serve()
