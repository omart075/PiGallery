import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";
import { useCallback } from "react";

export default function CustomParticles() {
    const config = {
        fullScreen: {
          zIndex: 1,
        },
        background: {
          color: "#000",
        },
        interactivity: {
            detectsOn: "window",
            events: {
                onhover: {
                    enable: true,
                    mode: "trail"
                },
                resize: true,
            },
            modes: {
                grab: {
                    distance: 400,
                    line_linked: {
                    opacity: 1,
                    },
                },
                bubble: {
                    distance: 400,
                    size: 40,
                    duration: 2,
                    opacity: 0.8,
                    speed: 3,
                },
                repulse: {
                    distance: 200,
                },
                push: {
                    particles_nb: 4,
                },
                remove: {
                    particles_nb: 2,
                },
                trail: {
                    delay: 0.005,
                    quantity: 1,
                    pauseOnStop: true,
                },
            },
        },
        retina_detect: true,
        fullScreen: {
            enable: true,
            zIndex: 100,
        },
        fpsLimit: 60,
        particles: {
            number: {
                value: 0,
                density: {
                    enable: true,
                    value_area: 800,
                },
            },
            color: {
                value: "#0080FF",
            },
            shape: {
                type: ["circle"],
            },
            opacity: {
                value: { min: 0, max: 1 },
                animation: {
                    enable: true,
                    speed: 1,
                    startValue: "max",
                    destroy: "min",
                },
            },
            size: {
                value: { min: 6, max: 12 },
            },
            links: {
                enable: false,
            },
            move: {
                enable: true,
                speed: 10.5,
                direction: "none",
                random: false,
                straight: false,
                outModes: {
                    default: "destroy",
                },
                attract: {
                    enable: false,
                    rotateX: 600,
                    rotateY: 1200,
                },
            },
        },
      };
     
    const particlesInit = useCallback(async (engine) => {
      // here we initialize the particles animation
      await loadFull(engine);
    }, []);

    return (
        <div className="CustomParticles">
          <Particles options={config} init={particlesInit} />
        </div>
      );
}