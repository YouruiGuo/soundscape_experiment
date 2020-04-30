s.boot;

({  var fn = "/home/vagrant/soundscape_experiment/audio/";
	var filenames = Array.with(fn++"forest.wav", fn++"jungle.wav", fn++"canoe_paddle.wav", fn++"ocean_noise.wav", fn++"beach.wav", fn++"seagull.wav", fn++"forest_evening.wav", fn++"night_camp.wav", fn++"cave_water_drops.wav", fn++"hard_rain.wav",fn++"distant_storm.wav", fn++"rain_tent.wav", fn++"car_rain.wav", fn++"rain.wav", fn++"city_rain.wav").postln;
	
	SynthDef(\playbuf,{
		arg out=0,bufnum=0, rate=1, trigger=1, startPos=0, loop=1, amp=1;
		var env;
		env = EnvGen.kr(Env.new([0.1, amp, amp, 0], [5, 42, 3]), \gate.tr);
		Out.ar(out,
			Pan2.ar(PlayBuf.ar(1,bufnum, BufRateScale.kr(bufnum)*rate, trigger, BufFrames.ir(bufnum)*startPos, loop)*env, 0.0);
		)
	}).add;
	~buffers = filenames.collect{ | item |
		Buffer.read(s, item);
	};
	5.0.wait;
	~synth = ~buffers.collect{ | buffer |
		Synth(\playbuf, [\out, 0, \bufnum, buffer.bufnum, \amp, 0, \gate, 0]);
	};

	x = OSCFunc( { | msg, time, addr, port |
		var pyFreq = msg;
		( "amp is " + pyFreq ).postln;
		~synth.do({
			arg item, i;
			~synth[i].set(\gate, -2);
			i.postln;
		});
		~synth.do({
			arg item, i;
			//~synth[i].set(\gate, 0);
			//if(msg[i+1]==0,{~synth[i].set(\gate, -2);});
			if(msg[i+1] > 0,{
				i.postln;
				~synth[i].set(\gate, 1, \amp, msg[i+1]);});
			});
	}, '/print' );

}.fork();
)

//s.freeAll;
