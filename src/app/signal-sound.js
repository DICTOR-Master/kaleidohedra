// Signal's sound (DICTO 2026-10-09: "a background noisy space signal, contact from another planet"):
// a soft hiss of deep-space static, slowly fading in and out, with the message's dots and dashes as
// tones riding on it, in time with the letters arriving. Off until the 🔊 button turns it on (phones
// need a tap before any sound anyway); only in Signal. Web Audio, all synthesised, no files.

const TONE_HZ = 640;
const RAMP = 0.006; // seconds: soft edges, no clicks

export function createSignalSound() {
  let ctx = null, master = null, toneGain = null, toneOn = false;

  function build() {
    ctx = new (globalThis.AudioContext || globalThis.webkitAudioContext)();
    master = ctx.createGain();
    master.gain.value = 0;
    master.connect(ctx.destination);

    // Static: looped white noise, band-limited like a far-off radio, its level drifting slowly.
    const len = ctx.sampleRate * 2;
    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    const noise = ctx.createBufferSource();
    noise.buffer = buf;
    noise.loop = true;
    const band = ctx.createBiquadFilter();
    band.type = 'bandpass';
    band.frequency.value = 1400;
    band.Q.value = 0.6;
    const hiss = ctx.createGain();
    hiss.gain.value = 0.12;
    const drift = ctx.createOscillator(); // the static breathes, about every 7 s
    drift.frequency.value = 0.14;
    const driftDepth = ctx.createGain();
    driftDepth.gain.value = 0.06;
    drift.connect(driftDepth).connect(hiss.gain);
    noise.connect(band).connect(hiss).connect(master);
    noise.start();
    drift.start();

    // The tone: a sine with a slight waver, through a narrow radio band.
    const osc = ctx.createOscillator();
    osc.type = 'sine';
    osc.frequency.value = TONE_HZ;
    const wobble = ctx.createOscillator();
    wobble.frequency.value = 5.5;
    const wobbleDepth = ctx.createGain();
    wobbleDepth.gain.value = 4; // Hz
    wobble.connect(wobbleDepth).connect(osc.frequency);
    toneGain = ctx.createGain();
    toneGain.gain.value = 0;
    const radio = ctx.createBiquadFilter();
    radio.type = 'bandpass';
    radio.frequency.value = TONE_HZ;
    radio.Q.value = 2;
    osc.connect(toneGain).connect(radio).connect(master);
    osc.start();
    wobble.start();
  }

  return {
    /** Sound on or off (call from a tap, so phones allow it). */
    setEnabled(on) {
      if (on && !ctx) build();
      if (!ctx) return;
      if (on) ctx.resume();
      const now = ctx.currentTime;
      master.gain.cancelScheduledValues(now);
      master.gain.setTargetAtTime(on ? 0.8 : 0, now, 0.15);
      if (!on) { toneOn = false; toneGain.gain.setTargetAtTime(0, now, RAMP); }
    },
    /** A dot or dash sounding now. */
    setTone(on) {
      if (!ctx || on === toneOn) return;
      toneOn = on;
      toneGain.gain.setTargetAtTime(on ? 0.35 : 0, ctx.currentTime, RAMP);
    },
  };
}
