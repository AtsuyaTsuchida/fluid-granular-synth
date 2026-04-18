// grain_mapper.js — simple version (no poly~)
// in:  list x y density vx vy
// out 0: [freq, 30]  → line~ (pitch ramp 30ms)
// out 1: [amp, 80]   → line~ (amplitude ramp 80ms)

inlets = 1;
outlets = 2;

function list() {
    var a = arrayfromargs(arguments);
    if (a.length < 5) return;

    var x       = a[0];
    var y       = a[1];
    var density = a[2];
    var vx      = a[3];
    var vy      = a[4];

    if (density < 0.05) return;

    var speed = Math.sqrt(vx * vx + vy * vy);
    var pitch = 48 + y * 24 + speed * 8.6;
    pitch = Math.max(36, Math.min(84, pitch));

    var freq = Math.pow(2, (pitch - 69) / 12) * 440;
    var amp  = density * 0.6;

    outlet(0, freq, 30);
    outlet(1, amp,  80);
}
