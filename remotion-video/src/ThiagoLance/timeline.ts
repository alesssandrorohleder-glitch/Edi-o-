// Frame numbers for "A hora do lance" (30 fps, 25 s). scripts/thiago_lance_sound.py reads the same values.

export const FPS = 30;
export const DURATION = 750;

// Camera travels envelope to envelope: E1 (hook), E2 (sorteio), E3 (lance, stamp, card).
export const PAN_TO_E2 = [100, 140] as const;
export const BALL = [128, 178] as const; // enters, stops on E2
export const FEINT = [184, 236] as const; // stamp dips over E2 and leaves
export const PAN_TO_E3 = [228, 268] as const;
export const WRITE_1 = [276, 318] as const; // "Outros, por lance."
export const WRITE_2 = [330, 376] as const; // "E tem quem saiba / a hora certa."
export const PEN_OUT = [380, 400] as const;
export const STAMP_IN = [398, 430] as const; // arrives high over E3
export const SILENCE = [404, 470] as const; // music out, only the clock
export const SLAM = 470; // contact
export const LIFT = [486, 520] as const;
export const CARD = [574, 660] as const; // card slides out of the envelope
export const CHECK = [690, 702] as const;
