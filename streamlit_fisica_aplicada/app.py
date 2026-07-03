import math
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

G = 6.67430e-11

st.set_page_config(
    page_title="Laboratorio de Física Aplicada",
    page_icon="🪐",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 35%, #020617 100%);
        color: #e5e7eb;
    }
    .block-container {padding-top: 1.3rem; padding-bottom: 2rem;}
    .hero {
        padding: 1.2rem 1.4rem;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(56,189,248,.18), rgba(34,197,94,.10));
        border: 1px solid rgba(148,163,184,.25);
        margin-bottom: 1rem;
    }
    .hero h1 {margin: 0; font-size: 2.2rem;}
    .hero p {color: #cbd5e1; margin-top: .4rem;}
    .card {
        padding: 1rem;
        border-radius: 18px;
        background: rgba(15,23,42,.78);
        border: 1px solid rgba(148,163,184,.22);
        margin-bottom: .8rem;
    }
    .small-muted {color: #94a3b8; font-size: .92rem;}
    div[data-testid="stMetric"] {
        background: rgba(15,23,42,.72);
        border: 1px solid rgba(148,163,184,.20);
        border-radius: 16px;
        padding: .7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@dataclass
class Body:
    name: str
    mass: float
    x: float
    y: float
    vx: float
    vy: float
    marker_size: int


def format_scientific(value: float, unit: str = "") -> str:
    return f"{value:.3e} {unit}".strip()


def make_figure(title: str, xlabel: str = "x (m)", ylabel: str = "y (m)", equal=True):
    fig, ax = plt.subplots(figsize=(8, 5.2))
    fig.patch.set_facecolor("#020617")
    ax.set_facecolor("#020617")
    ax.tick_params(colors="#cbd5e1")
    ax.xaxis.label.set_color("#cbd5e1")
    ax.yaxis.label.set_color("#cbd5e1")
    ax.title.set_color("#e5e7eb")
    for spine in ax.spines.values():
        spine.set_color("#334155")
    ax.grid(True, alpha=0.25)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if equal:
        ax.axis("equal")
    return fig, ax


def page_header():
    st.markdown(
        """
        <div class="hero">
            <h1>🪐 Laboratorio de Física Aplicada</h1>
            <p>Simulador interactivo para estudiar ecuaciones del movimiento, leyes de Newton y gravitación universal.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def movimiento_general():
    st.subheader("🚀 Tema 1: Ecuaciones generales del movimiento")
    st.markdown(
        """
        <div class="card">
        <b>Idea principal:</b> la posición cambia por la velocidad, y la velocidad cambia por la aceleración.
        Si conoces el estado inicial de un cuerpo, puedes predecir su movimiento paso a paso.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📘 Fórmulas usadas", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.latex(r"\vec r_f = \vec r_i + \vec v_i t + \frac{1}{2}\vec a t^2")
        c2.latex(r"\vec v_f = \vec v_i + \vec a t")
        c3.latex(r"\Delta \vec r = \vec r_f - \vec r_i")

    left, right = st.columns([1, 1.25])

    with left:
        st.markdown("### Datos iniciales")
        example = st.selectbox(
            "Ejemplo rápido",
            [
                "Movimiento con gravedad",
                "Movimiento rectilíneo uniforme",
                "Desplazamiento A(-1,2) a B(3,-2)",
                "Personalizado",
            ],
        )

        if example == "Movimiento rectilíneo uniforme":
            defaults = (-1.0, 2.0, 4.0, -4.0, 0.0, 0.0, 1.0)
        elif example == "Desplazamiento A(-1,2) a B(3,-2)":
            defaults = (-1.0, 2.0, 4.0, -4.0, 0.0, 0.0, 1.0)
        else:
            defaults = (0.0, 0.0, 12.0, 18.0, 0.0, -9.8, 4.0)

        x0 = st.number_input("x₀ posición inicial (m)", value=defaults[0])
        y0 = st.number_input("y₀ posición inicial (m)", value=defaults[1])
        vx0 = st.number_input("vx₀ velocidad inicial (m/s)", value=defaults[2])
        vy0 = st.number_input("vy₀ velocidad inicial (m/s)", value=defaults[3])
        ax = st.number_input("ax aceleración (m/s²)", value=defaults[4])
        ay = st.number_input("ay aceleración (m/s²)", value=defaults[5])
        t_total = st.number_input("Tiempo total t (s)", min_value=0.01, value=defaults[6])
        puntos = st.slider("Puntos de la simulación", 20, 600, 160)

    t = np.linspace(0, t_total, puntos)
    x = x0 + vx0 * t + 0.5 * ax * t**2
    y = y0 + vy0 * t + 0.5 * ay * t**2
    vx_f = vx0 + ax * t_total
    vy_f = vy0 + ay * t_total
    speed_f = math.sqrt(vx_f**2 + vy_f**2)
    displacement = math.sqrt((x[-1] - x0) ** 2 + (y[-1] - y0) ** 2)

    with right:
        st.markdown("### Resultados")
        m1, m2, m3 = st.columns(3)
        m1.metric("Posición final", f"({x[-1]:.2f}, {y[-1]:.2f}) m")
        m2.metric("Velocidad final", f"{speed_f:.2f} m/s")
        m3.metric("Desplazamiento", f"{displacement:.2f} m")

        fig, axp = make_figure("Trayectoria del cuerpo")
        axp.plot(x, y, linewidth=2.2, label="Trayectoria")
        axp.scatter([x0], [y0], s=85, label="Inicio")
        axp.scatter([x[-1]], [y[-1]], s=85, label="Final")
        axp.quiver(x0, y0, vx0, vy0, angles="xy", scale_units="xy", scale=1, width=0.006, label="v inicial")
        axp.legend(facecolor="#0f172a", edgecolor="#334155", labelcolor="#e5e7eb")
        st.pyplot(fig)

    with st.expander("🧠 Procedimiento para explicar en clase"):
        st.write(f"1. Se define la posición inicial: r₀ = ({x0}, {y0}) m.")
        st.write(f"2. Se define la velocidad inicial: v₀ = ({vx0}, {vy0}) m/s.")
        st.write(f"3. Se aplica la aceleración: a = ({ax}, {ay}) m/s².")
        st.write(f"4. Se calcula la posición final con r = r₀ + v₀t + ½at² para t = {t_total} s.")
        st.write(f"5. Se calcula la velocidad final con v = v₀ + at.")
        st.write(f"6. Resultado final: r = ({x[-1]:.2f}, {y[-1]:.2f}) m y v = ({vx_f:.2f}, {vy_f:.2f}) m/s.")


def gravitational_force_panel():
    st.markdown("### 🧲 Calculadora de fuerza gravitacional")
    c1, c2, c3 = st.columns(3)
    with c1:
        m1 = st.number_input("Masa 1 m₁ (kg)", value=1.989e30, format="%.6e")
    with c2:
        m2 = st.number_input("Masa 2 m₂ (kg)", value=5.972e24, format="%.6e")
    with c3:
        r = st.number_input("Distancia r (m)", min_value=1.0, value=1.50e11, format="%.6e")

    force = G * m1 * m2 / r**2
    accel_2 = force / m2
    accel_1 = force / m1
    k1, k2, k3 = st.columns(3)
    k1.metric("Fuerza F", format_scientific(force, "N"))
    k2.metric("Aceleración de m₂", format_scientific(accel_2, "m/s²"))
    k3.metric("Aceleración de m₁", format_scientific(accel_1, "m/s²"))


def simulate_orbit(central_mass: float, orbit_mass: float, radius: float, v0: float, days: int, dt_hours: float):
    dt = dt_hours * 3600
    total_time = days * 24 * 3600
    steps = max(2, int(total_time / dt))

    pos = np.array([radius, 0.0], dtype=float)
    vel = np.array([0.0, v0], dtype=float)
    xs, ys, speeds, energies = [], [], [], []

    for _ in range(steps):
        dist = np.linalg.norm(pos)
        acc = -G * central_mass * pos / dist**3
        vel = vel + acc * dt
        pos = pos + vel * dt
        xs.append(pos[0])
        ys.append(pos[1])
        speeds.append(np.linalg.norm(vel))
        kinetic = 0.5 * orbit_mass * np.linalg.norm(vel) ** 2
        potential = -G * central_mass * orbit_mass / dist
        energies.append(kinetic + potential)

    return np.array(xs), np.array(ys), np.array(speeds), np.array(energies)


def gravitacion_universal():
    st.subheader("🌍 Tema 2: Ley de Gravitación Universal")
    st.markdown(
        """
        <div class="card">
        <b>Idea principal:</b> dos masas se atraen. Mientras mayor sea la masa, mayor será la fuerza;
        mientras mayor sea la distancia, menor será la fuerza. Esa fuerza produce aceleración y cambia la trayectoria.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📘 Fórmulas usadas", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.latex(r"F = G\frac{m_1m_2}{r^2}")
        c2.latex(r"\vec a = -G\frac{M}{r^3}\vec r")
        c3.latex(r"v = \frac{2\pi r}{T}")

    gravitational_force_panel()
    st.divider()

    left, right = st.columns([1, 1.35])
    with left:
        st.markdown("### Simulación orbital")
        preset = st.selectbox("Sistema", ["Tierra alrededor del Sol", "Luna alrededor de la Tierra", "Personalizado"])

        if preset == "Tierra alrededor del Sol":
            central_name, orbit_name = "Sol", "Tierra"
            central_mass, orbit_mass = 1.989e30, 5.972e24
            radius, period = 1.50e11, 365 * 24 * 3600
            days_default, dt_default = 365, 12
        elif preset == "Luna alrededor de la Tierra":
            central_name, orbit_name = "Tierra", "Luna"
            central_mass, orbit_mass = 5.972e24, 7.348e22
            radius, period = 3.844e8, 27.3 * 24 * 3600
            days_default, dt_default = 28, 1
        else:
            central_name, orbit_name = "Cuerpo central", "Cuerpo en órbita"
            central_mass, orbit_mass = 1.989e30, 5.972e24
            radius, period = 1.50e11, 365 * 24 * 3600
            days_default, dt_default = 365, 12

        central_mass = st.number_input("Masa del cuerpo central M (kg)", value=float(central_mass), format="%.6e")
        orbit_mass = st.number_input("Masa del cuerpo en órbita m (kg)", value=float(orbit_mass), format="%.6e")
        radius = st.number_input("Radio/distancia inicial r (m)", min_value=1.0, value=float(radius), format="%.6e")
        period = st.number_input("Periodo orbital T (s)", min_value=1.0, value=float(period), format="%.6e")
        days = st.slider("Días simulados", 1, 730, days_default)
        dt_hours = st.slider("Paso de tiempo dt (horas)", 0.25, 48.0, float(dt_default), step=0.25)

        v_orbital = 2 * math.pi * radius / period
        v_escape = math.sqrt(2 * G * central_mass / radius)
        velocity_factor = st.slider("Factor de velocidad inicial", 0.50, 1.50, 1.00, 0.01)
        v0 = v_orbital * velocity_factor

    xs, ys, speeds, energies = simulate_orbit(central_mass, orbit_mass, radius, v0, days, dt_hours)
    force = G * central_mass * orbit_mass / radius**2
    acceleration = force / orbit_mass

    with right:
        k1, k2, k3 = st.columns(3)
        k1.metric("Velocidad circular", f"{v_orbital:,.2f} m/s")
        k2.metric("Velocidad inicial usada", f"{v0:,.2f} m/s")
        k3.metric("Fuerza inicial", format_scientific(force, "N"))

        fig, axp = make_figure("Órbita simulada", "x", "y")
        scale = 1e9 if radius > 1e10 else 1e6
        unit = "10⁹ m" if scale == 1e9 else "10⁶ m"
        axp.plot(xs / scale, ys / scale, linewidth=2.1, label=f"{orbit_name}")
        axp.scatter([0], [0], s=160, label=central_name)
        axp.scatter([xs[-1] / scale], [ys[-1] / scale], s=75, label="Posición final")
        axp.set_xlabel(f"x ({unit})")
        axp.set_ylabel(f"y ({unit})")
        axp.legend(facecolor="#0f172a", edgecolor="#334155", labelcolor="#e5e7eb")
        st.pyplot(fig)

        with st.expander("📉 Ver velocidad y energía de la simulación"):
            fig2, ax2 = make_figure("Velocidad durante la simulación", "Paso", "m/s", equal=False)
            ax2.plot(speeds, linewidth=2)
            st.pyplot(fig2)

            fig3, ax3 = make_figure("Energía mecánica aproximada", "Paso", "J", equal=False)
            ax3.plot(energies, linewidth=2)
            st.pyplot(fig3)

    with st.expander("🧠 Procedimiento para explicar en clase"):
        st.write("1. Se define un cuerpo central y un cuerpo que orbita alrededor de él.")
        st.write("2. Se calcula la fuerza inicial con F = G·M·m/r².")
        st.write(f"3. Con esa fuerza se obtiene la aceleración inicial: a = F/m = {acceleration:.3e} m/s².")
        st.write("4. Se calcula una velocidad circular aproximada con v = 2πr/T.")
        st.write("5. En cada paso dt, la aceleración gravitacional cambia la velocidad y luego la posición.")
        st.write("6. Al guardar cada posición, se obtiene la trayectoria orbital que aparece en la gráfica.")
        st.write("7. Si modificas el factor de velocidad, puedes observar órbitas más abiertas, cerradas o inestables.")


def comparacion_newton():
    st.subheader("⚖️ Leyes de Newton conectadas con la simulación")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
        <h4>Primera Ley</h4>
        Un cuerpo mantiene su estado de reposo o movimiento rectilíneo uniforme si no actúa una fuerza neta externa.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card">
        <h4>Segunda Ley</h4>
        La fuerza neta produce aceleración: F = m·a. Esta es la base para actualizar la velocidad.
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card">
        <h4>Tercera Ley</h4>
        Si un cuerpo atrae a otro, recibe una fuerza igual en magnitud y opuesta en dirección.
        </div>
        """, unsafe_allow_html=True)

    st.info("La simulación usa especialmente la Segunda Ley de Newton: primero calcula fuerza, luego aceleración, después velocidad y finalmente posición.")


def main():
    page_header()
    st.sidebar.title("📚 Menú")
    section = st.sidebar.radio(
        "Selecciona una sección",
        ["Ecuaciones del movimiento", "Gravitación universal", "Leyes de Newton", "Guía para explicar"],
    )

    st.sidebar.divider()
    st.sidebar.caption("Proyecto de Física Aplicada")
    st.sidebar.caption("Streamlit + NumPy + Matplotlib")

    if section == "Ecuaciones del movimiento":
        movimiento_general()
    elif section == "Gravitación universal":
        gravitacion_universal()
    elif section == "Leyes de Newton":
        comparacion_newton()
    else:
        st.subheader("🎤 Guía rápida para defender el proyecto")
        st.markdown(
            """
            <div class="card">
            <b>Explicación corta:</b> esta página simula movimiento usando vectores. Primero se ingresan posición,
            velocidad, aceleración, masa y distancia. Luego el programa aplica las fórmulas físicas para calcular
            resultados y graficar la trayectoria.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("""
        ### Orden recomendado para explicar
        1. La posición indica dónde está el cuerpo.
        2. La velocidad indica cómo cambia la posición.
        3. La aceleración indica cómo cambia la velocidad.
        4. Según Newton, la fuerza produce aceleración.
        5. En gravitación, la fuerza aparece porque dos masas se atraen.
        6. La computadora repite esos cálculos muchas veces y por eso aparece una trayectoria.
        """)

        st.success("Frase clave: no estamos dibujando la órbita manualmente; la órbita aparece porque actualizamos posición y velocidad paso a paso.")


if __name__ == "__main__":
    main()
