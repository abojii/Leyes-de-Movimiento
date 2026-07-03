import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Física Aplicada", page_icon="🪐", layout="wide")

st.markdown("""
<style>
.stApp { background: #0e1117; color: white; }
.block-container { padding-top: 1.5rem; }
[data-testid="stMetricValue"] { font-size: 1.4rem; }
</style>
""", unsafe_allow_html=True)

G = 6.67430e-11

st.title("🪐 Simulador de Física Aplicada")
st.caption("Ecuaciones generales del movimiento y Ley de Gravitación Universal")


def plot_2d_path(x, y, title, xlabel="x (m)", ylabel="y (m)"):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(x, y, marker="o", markersize=2)
    ax.scatter([x[0]], [y[0]], s=70, label="Inicio")
    ax.scatter([x[-1]], [y[-1]], s=70, label="Final")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    ax.axis("equal")
    ax.legend()
    st.pyplot(fig)


def movimiento_rectilineo():
    st.subheader("📌 Ecuaciones generales del movimiento")
    st.write("Aquí usamos las relaciones básicas: posición, velocidad y aceleración. La idea es calcular cómo cambia un cuerpo con el tiempo.")

    st.latex(r"\vec r_f = \vec r_i + \vec v \cdot t")
    st.latex(r"\vec v_f = \vec v_i + \vec a \cdot t")
    st.latex(r"\vec r_f = \vec r_i + \vec v_i t + \frac{1}{2}\vec a t^2")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Datos iniciales")
        x0 = st.number_input("Posición inicial x₀ (m)", value=-1.0)
        y0 = st.number_input("Posición inicial y₀ (m)", value=2.0)
        vx0 = st.number_input("Velocidad inicial vx (m/s)", value=4.0)
        vy0 = st.number_input("Velocidad inicial vy (m/s)", value=-4.0)
    with col2:
        st.markdown("### Aceleración y tiempo")
        ax = st.number_input("Aceleración ax (m/s²)", value=0.0)
        ay = st.number_input("Aceleración ay (m/s²)", value=-9.8)
        t_total = st.number_input("Tiempo total (s)", min_value=0.1, value=2.0)
        pasos = st.slider("Cantidad de puntos", 10, 500, 100)

    t = np.linspace(0, t_total, pasos)
    x = x0 + vx0 * t + 0.5 * ax * t**2
    y = y0 + vy0 * t + 0.5 * ay * t**2
    vx = vx0 + ax * t_total
    vy = vy0 + ay * t_total

    c1, c2, c3 = st.columns(3)
    c1.metric("x final", f"{x[-1]:.2f} m")
    c2.metric("y final", f"{y[-1]:.2f} m")
    c3.metric("v final", f"({vx:.2f}, {vy:.2f}) m/s")

    plot_2d_path(x, y, "Trayectoria del cuerpo")

    with st.expander("Procedimiento paso a paso"):
        st.write(f"1. Se parte de la posición inicial r₀ = ({x0}, {y0}) m.")
        st.write(f"2. Se usa la velocidad inicial v₀ = ({vx0}, {vy0}) m/s.")
        st.write(f"3. Se aplica la aceleración a = ({ax}, {ay}) m/s².")
        st.write(f"4. Para t = {t_total} s, se calcula la posición final con r = r₀ + v₀t + ½at².")
        st.write(f"5. Resultado: r = ({x[-1]:.2f}, {y[-1]:.2f}) m y v = ({vx:.2f}, {vy:.2f}) m/s.")


def gravitacion():
    st.subheader("🌍 Ley de Gravitación Universal")
    st.write("Esta parte calcula la fuerza gravitatoria entre dos cuerpos y simula una órbita simple en 2D.")

    st.latex(r"F = G\frac{m_1m_2}{r^2}")
    st.latex(r"a = \frac{F}{m} = G\frac{M}{r^2}")
    st.latex(r"v = \frac{2\pi r}{T}")

    preset = st.selectbox("Ejemplo rápido", ["Tierra alrededor del Sol", "Luna alrededor de la Tierra", "Personalizado"])

    if preset == "Tierra alrededor del Sol":
        M_default, m_default, r_default, T_default = 1.989e30, 5.972e24, 150e9, 365 * 24 * 3600
    elif preset == "Luna alrededor de la Tierra":
        M_default, m_default, r_default, T_default = 5.972e24, 7.348e22, 384400e3, 27.3 * 24 * 3600
    else:
        M_default, m_default, r_default, T_default = 1.989e30, 5.972e24, 150e9, 365 * 24 * 3600

    col1, col2 = st.columns(2)
    with col1:
        M = st.number_input("Masa del cuerpo central M (kg)", value=float(M_default), format="%.6e")
        m = st.number_input("Masa del cuerpo en órbita m (kg)", value=float(m_default), format="%.6e")
        r = st.number_input("Distancia inicial r (m)", value=float(r_default), format="%.6e")
    with col2:
        T = st.number_input("Periodo orbital T (s)", value=float(T_default), format="%.6e")
        dias = st.slider("Días a simular", 1, 730, 365)
        dt_horas = st.slider("Paso de tiempo dt (horas)", 1, 48, 6)

    F = G * M * m / r**2
    a = F / m
    v_circular = 2 * np.pi * r / T

    c1, c2, c3 = st.columns(3)
    c1.metric("Fuerza gravitatoria", f"{F:.3e} N")
    c2.metric("Aceleración", f"{a:.3e} m/s²")
    c3.metric("Velocidad orbital", f"{v_circular:.2f} m/s")

    dt = dt_horas * 3600
    steps = int((dias * 24 * 3600) / dt)
    pos = np.array([r, 0.0], dtype=float)
    vel = np.array([0.0, v_circular], dtype=float)
    xs, ys = [], []

    for _ in range(max(1, steps)):
        dist = np.linalg.norm(pos)
        acc = -G * M * pos / dist**3
        vel = vel + acc * dt
        pos = pos + vel * dt
        xs.append(pos[0])
        ys.append(pos[1])

    fig, axp = plt.subplots(figsize=(7, 7))
    axp.plot(np.array(xs) / 1e9, np.array(ys) / 1e9)
    axp.scatter([0], [0], s=120, label="Cuerpo central")
    axp.scatter([xs[-1] / 1e9], [ys[-1] / 1e9], s=60, label="Posición final")
    axp.set_title("Simulación orbital aproximada")
    axp.set_xlabel("x (10⁹ m)")
    axp.set_ylabel("y (10⁹ m)")
    axp.grid(True)
    axp.axis("equal")
    axp.legend()
    st.pyplot(fig)

    with st.expander("Procedimiento paso a paso"):
        st.write("1. Se calcula la fuerza de atracción gravitatoria con F = G·M·m/r².")
        st.write("2. Se despeja la aceleración del cuerpo en órbita usando a = F/m.")
        st.write("3. Se estima la velocidad orbital con v = 2πr/T.")
        st.write("4. En cada intervalo dt se actualiza primero la velocidad y luego la posición.")
        st.write("5. Las posiciones guardadas se grafican para observar la trayectoria.")


tab1, tab2 = st.tabs(["Ecuaciones del movimiento", "Gravitación universal"])
with tab1:
    movimiento_rectilineo()
with tab2:
    gravitacion()

st.divider()
st.info("Tip: para explicar el proyecto, di que la simulación usa vectores de posición, velocidad y aceleración para actualizar el movimiento paso a paso.")
