import React from 'react';

type P = {name: string; size?: number; color?: string; stroke?: number; progress?: number};

// Ícones de traço (stroke) desenhados em SVG — nada de imagens prontas.
const paths: Record<string, string[]> = {
  plane: ['M3 13l7-2 4-7 2 1-2 6 5-1 2-2 1 1-2 4-11 4-4-1z', 'M7 19h10'],
  car: ['M3 15l2-6a2 2 0 0 1 2-1.5h10A2 2 0 0 1 19 9l2 6v3h-2.5', 'M5.5 18H3v-3h18', 'M7.5 18a1.5 1.5 0 1 0 0 .01', 'M16.5 18a1.5 1.5 0 1 0 0 .01', 'M9 18h6'],
  shield: ['M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z', 'M8.5 12l2.5 2.5 4.5-5'],
  lock: ['M6 11h12v9H6z', 'M8.5 11V8a3.5 3.5 0 0 1 7 0v3', 'M12 15v2'],
  back: ['M15 5l-7 7 7 7'],
  home: ['M4 11l8-7 8 7v9h-5v-6H9v6H4z'],
  chart: ['M4 20V10', 'M10 20V4', 'M16 20v-7', 'M22 20H2'],
  plus: ['M12 5v14', 'M5 12h14'],
  user: ['M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8z', 'M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6'],
  del: ['M9 6h11v12H9l-6-6z', 'M12 10l4 4', 'M16 10l-4 4'],
  film: ['M4 5h16v14H4z', 'M8 5v14', 'M16 5v14', 'M4 9h4', 'M4 15h4', 'M16 9h4', 'M16 15h4'],
  play: ['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z', 'M10 8.5l5.5 3.5-5.5 3.5z'],
  phone: ['M7 3h10a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z', 'M10 18h4', 'M9 8h6', 'M9 11h4'],
  spark: ['M12 3l2.2 6.8L21 12l-6.8 2.2L12 21l-2.2-6.8L3 12l6.8-2.2z'],
};

export const Icon: React.FC<P> = ({name, size = 48, color = '#fff', stroke = 2, progress = 1}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" style={{display: 'block'}}>
    {(paths[name] || []).map((d, i) => (
      <path
        key={i}
        d={d}
        stroke={color}
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeLinejoin="round"
        pathLength={1}
        strokeDasharray={1}
        strokeDashoffset={1 - progress}
      />
    ))}
  </svg>
);
