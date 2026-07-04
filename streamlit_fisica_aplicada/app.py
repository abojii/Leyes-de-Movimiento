import time
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Física Aplicada",
    page_icon="🌌",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #090d18;
    color: white;
}
h1, h2, h3 {
    color: #ff5fa2;
}
[data-testid="stSidebar"] {
    background-color: #0f1626;
}
.stButton button {
    background-color: #ff5fa2;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}
.stButton button:hover {
    background-color: #ff2f86;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🌌 Física Aplicada")
st.write("Simulación interactiva de Leyes del Movimiento y Gravitación Universal.")

menu = st.sidebar.radio(
    "Selecciona un tema:",
    [
        "Inicio",
        "Leyes del Movimiento",
        "Gravitación Universal"
    ]
)

if menu == "Inicio":
    st.header("Bienvenida")
    st.write("""
    Esta aplicación permite estudiar dos temas principales de Física Aplicada:

    1. **Leyes del Movimiento**
    2. **Ley de Gravitación Universal**

    El usuario puede ingresar datos, calcular resultados y observar gráficas interactivas.
    """)

elif menu == "Leyes del Movimiento":
    st.header("📘 Leyes del Movimiento")

    st.write("""
    En esta sección se calcula la posición final de un cuerpo usando su posición inicial,
    velocidad, aceleración y tiempo.
    """)

    st.latex(r"\vec{r_f} = \vec{r_i} + \vec{v_i}t + \frac{1}{2}\vec{a}t^2")
    st.latex(r"\vec{v_f} = \vec{v_i} + \vec{a}t")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos de entrada")

        x0 = st.number_input("Posición inicial en X (m)", value=0.0)
        y0 = st.number_input("Posición inicial en Y (m)", value=0.0)

        vx0 = st.number_input("Velocidad inicial en X (m/s)", value=10.0)
        vy0 = st.number_input("Velocidad inicial en Y (m/s)", value=20.0)

        ax = st.number_input("Aceleración en X (m/s²)", value=0.0)
        ay = st.number_input("Aceleración en Y (m/s²)", value=-9.8)

        t = st.number_input("Tiempo total (s)", min_value=0.1, value=5.0)

    with col2:
        st.subheader("Resultados")

        xf = x0 + vx0 * t + 0.5 * ax * t**2
        yf = y0 + vy0 * t + 0.5 * ay * t**2

        vxf = vx0 + ax * t
        vyf = vy0 + ay * t

        st.metric("Posición final X", f"{xf:.2f} m")
        st.metric("Posición final Y", f"{yf:.2f} m")
        st.metric("Velocidad final X", f"{vxf:.2f} m/s")
        st.metric("Velocidad final Y", f"{vyf:.2f} m/s")

    st.subheader("Trayectoria del movimiento")

    tiempos = np.linspace(0, t, 100)
    x = x0 + vx0 * tiempos + 0.5 * ax * tiempos**2
    y = y0 + vy0 * tiempos + 0.5 * ay * tiempos**2

    fig, ax_plot = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("#090d18")
    ax_plot.set_facecolor("#090d18")

    ax_plot.plot(x, y, color="#ff5fa2", linewidth=2, label="Trayectoria")
    ax_plot.scatter(x0, y0, color="cyan", s=80, label="Inicio")
    ax_plot.scatter(xf, yf, color="orange", s=80, label="Final")

    ax_plot.set_title("Trayectoria del cuerpo", color="white")
    ax_plot.set_xlabel("Posición X (m)", color="white")
    ax_plot.set_ylabel("Posición Y (m)", color="white")
    ax_plot.tick_params(colors="white")
    ax_plot.grid(True, alpha=0.3)
    ax_plot.legend()

    st.pyplot(fig)
    plt.close(fig)

elif menu == "Gravitación Universal":
    st.header("🌍 Ley de Gravitación Universal")

    st.write("""
    En esta sección se simula el movimiento de un cuerpo orbitando alrededor de una masa central.
    Por ejemplo, la Tierra alrededor del Sol.
    """)

    st.latex(r"F = G \frac{m_1m_2}{r^2}")
    st.latex(r"a = \frac{F}{m}")
    st.latex(r"v_f = v_i + a \Delta t")
    st.latex(r"r_f = r_i + v \Delta t")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parámetros")

        masa_central = st.number_input(
            "Masa central M (kg)",
            min_value=1e20,
            value=1.989e30,
            format="%.3e"
        )

        masa_orbitante = st.number_input(
            "Masa orbitante m (kg)",
            min_value=1e10,
            value=5.972e24,
            format="%.3e"
        )

        distancia_inicial = st.number_input(
            "Distancia inicial r₀ (m)",
            min_value=1e7,
            value=1.496e11,
            format="%.3e"
        )

        velocidad_inicial = st.number_input(
            "Velocidad inicial tangencial v₀ (m/s)",
            min_value=0.0,
            value=29780.0,
            format="%.2f"
        )

        paso_tiempo = st.number_input(
            "Paso de tiempo Δt (s)",
            min_value=1.0,
            value=3600.0,
            format="%.0f"
        )

        tiempo_total = st.number_input(
            "Tiempo total (días)",
            min_value=1.0,
            value=365.0,
            format="%.0f"
        )

        animar = st.button("▶ Animar órbita")

    G = 6.67430e-11

    n = int((tiempo_total * 24 * 3600) / paso_tiempo)

    x = distancia_inicial
    y = 0.0

    vx = 0.0
    vy = velocidad_inicial

    x_data = []
    y_data = []

    for i in range(n):
        r = np.sqrt(x**2 + y**2)

        ax_g = -G * masa_central * x / r**3
        ay_g = -G * masa_central * y / r**3

        vx += ax_g * paso_tiempo
        vy += ay_g * paso_tiempo

        x += vx * paso_tiempo
        y += vy * paso_tiempo

        x_data.append(x)
        y_data.append(y)

    x_data = np.array(x_data)
    y_data = np.array(y_data)

    with col2:
        st.subheader("Órbita simulada")

        grafica = st.empty()

        limite = distancia_inicial / 1e9 * 1.4

        def dibujar_orbita(indice):
            fig, ax = plt.subplots(figsize=(7, 7))

            fig.patch.set_facecolor("#090d18")
            ax.set_facecolor("#090d18")

            ax.plot(
                x_data[:indice] / 1e9,
                y_data[:indice] / 1e9,
                color="#1f77b4",
                linewidth=2,
                label="Trayectoria"
            )

            ax.scatter(
                0,
                0,
                color="#1f77b4",
                s=160,
                label="Masa central"
            )

            ax.scatter(
                x_data[indice - 1] / 1e9,
                y_data[indice - 1] / 1e9,
                color="#ff7f0e",
                s=80,
                label="Cuerpo orbitante"
            )

            ax.set_title("Órbita simulada", color="white")
            ax.set_xlabel("x (10⁹ m)", color="white")
            ax.set_ylabel("y (10⁹ m)", color="white")

            ax.set_xlim(-limite, limite)
            ax.set_ylim(-limite, limite)

            ax.set_aspect("equal")
            ax.tick_params(colors="white")
            ax.grid(True, alpha=0.3)
            ax.legend()

            grafica.pyplot(fig)
            plt.close(fig)

        if animar:
            salto = max(1, len(x_data) // 250)

            for i in range(1, len(x_data), salto):
                dibujar_orbita(i)
                time.sleep(0.03)

            dibujar_orbita(len(x_data))

        else:
            dibujar_orbita(len(x_data))

    st.subheader("Resultados")

    fuerza_inicial = G * masa_central * masa_orbitante / distancia_inicial**2
    aceleracion_inicial = fuerza_inicial / masa_orbitante

    distancia_final = np.sqrt(x_data[-1]**2 + y_data[-1]**2)

    colr1, colr2, colr3 = st.columns(3)

    with colr1:
        st.metric("Fuerza gravitatoria inicial", f"{fuerza_inicial:.3e} N")

    with colr2:
        st.metric("Aceleración inicial", f"{aceleracion_inicial:.3e} m/s²")

    with colr3:
        st.metric("Distancia final", f"{distancia_final:.3e} m")

    st.subheader("Procedimiento")

    st.write("""
    1. Se coloca el cuerpo orbitante a una distancia inicial de la masa central.
    2. Se calcula la distancia entre ambos cuerpos.
    3. Se aplica la Ley de Gravitación Universal.
    4. Se obtiene la aceleración usando la Segunda Ley de Newton.
    5. Se actualiza la velocidad.
    6. Se actualiza la posición.
    7. Se repite el proceso muchas veces para formar la trayectoria.
    """)