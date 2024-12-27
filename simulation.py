# Import necessary libraries
import numpy as np
from scipy.integrate import solve_ivp
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Constants
epsilon_0 = 8.85e-12  # Permittivity of free space (F/m)
k = 1 / (4 * np.pi * epsilon_0)  # Coulomb's constant (N m²/C²)

# Electric Potential
def electric_potential(x, y, t, q_particle, Omega, q_field):
    Phi = 0
    charges = {
        (10.0, 10.0): q_field,
        (-10.0, -10.0): q_field,
        (-10.0, 10.0): -q_field,
        (10.0, -10.0): -q_field,
    }
    for (x_i, y_i), sign in charges.items():
        r = np.sqrt((x - x_i)**2 + (y - y_i)**2)
        if r != 0:
            Q = sign * q_particle * np.cos(Omega * t)
            Phi += k * Q / r
    return Phi

# Electric Field from Potential
def electric_field_from_potential(x, y, t, q_particle, Omega, q_field, dx=1e-6):
    Ex = -(electric_potential(x + dx, y, t, q_particle, Omega, q_field) - 
           electric_potential(x - dx, y, t, q_particle, Omega, q_field)) / (2 * dx)
    Ey = -(electric_potential(x, y + dx, t, q_particle, Omega, q_field) - 
           electric_potential(x, y - dx, t, q_particle, Omega, q_field)) / (2 * dx)
    return Ex, Ey

# Equations of Motion
def equations_of_motion_potential(t, state, q_particle, m_particle, Omega, q_field):
    x, y, vx, vy = state
    Ex, Ey = electric_field_from_potential(x, y, t, q_particle, Omega, q_field)
    ax = (q_particle / m_particle) * Ex
    ay = (q_particle / m_particle) * Ey
    return [vx, vy, ax, ay]

# Initialize Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("2D Quadrupole Paul Trap Simulation"),
    
    dcc.Graph(id='trajectory-graph'),

    html.Div([
        dcc.Slider(id='x0', min=-10, max=10, step=0.1, value=2, tooltip={"placement": "bottom"}),
        html.Label("Initial x0 (m)"),

        dcc.Slider(id='y0', min=-10, max=10, step=0.1, value=5, tooltip={"placement": "bottom"}),
        html.Label("Initial y0 (m)"),

        dcc.Slider(id='vx0', min=-5, max=5, step=0.1, value=1, tooltip={"placement": "bottom"}),
        html.Label("Initial vx0 (m/s)"),

        dcc.Slider(id='vy0', min=-5, max=5, step=0.1, value=-1, tooltip={"placement": "bottom"}),
        html.Label("Initial vy0 (m/s)"),

        dcc.Input(id='q_particle', type='number', value=1.6e-19, step=1e-20),
        html.Label("Particle Charge (C)"),

        dcc.Input(id='m_particle', type='number', value=1.67e-27, step=1e-28),
        html.Label("Particle Mass (kg)"),

        dcc.Slider(id='Omega', min=1e5, max=1e6, step=1e4, value=2 * np.pi * 2e5, tooltip={"placement": "bottom"}),
        html.Label("Omega (rad/s)"),

        dcc.Input(id='q_field', type='number', value=1.6e-19, step=1e-20),
        html.Label("Field Charge (C)")
    ])
])

# Update Callback
@app.callback(
    Output('trajectory-graph', 'figure'),
    Input('x0', 'value'),
    Input('y0', 'value'),
    Input('vx0', 'value'),
    Input('vy0', 'value'),
    Input('q_particle', 'value'),
    Input('m_particle', 'value'),
    Input('Omega', 'value'),
    Input('q_field', 'value')
)
def update_graph(x0, y0, vx0, vy0, q_particle, m_particle, Omega, q_field):
    initial_conditions = [x0, y0, vx0, vy0]
    simulation_time = 1e-4
    num_steps = 1000

    # Solve the equations of motion
    solution = solve_ivp(
        equations_of_motion_potential,
        t_span=(0, simulation_time),
        y0=initial_conditions,
        method='RK45',
        t_eval=np.linspace(0, simulation_time, num_steps),
        rtol=1e-9,
        atol=1e-12,
        args=(q_particle, m_particle, Omega, q_field)
    )

    # Extract results
    x_traj, y_traj = solution.y[0], solution.y[1]

    # Plot the trajectory
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_traj, y=y_traj, mode='lines', name='Trajectory'))
    fig.update_layout(
        title="2D Quadrupole Paul Trap Trajectory",
        xaxis_title="x (m)",
        yaxis_title="y (m)",
        width=800,
        height=600
    )
    return fig

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)