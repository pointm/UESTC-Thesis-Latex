(* ::Package:: *)

(* \:5b9a\:4e49\:771f\:7a7a\:4ecb\:8d28\:53c2\:6570 *)
c = 3*^8; (* \:5149\:901f\:ff0c\:5355\:4f4d\:ff1am/s *)
a = 35/1000; (* \:6ce2\:5bfc\:534a\:5f84\:ff0c\:5355\:4f4d\:ff1a\:7c73 *)
\[Mu] = 1; (* \:771f\:7a7a\:78c1\:5bfc\:7387\:ff0c\:5355\:4f4d\:ff1aH/m *)
\[CurlyEpsilon] = 1; (* \:771f\:7a7a\:4ecb\:7535\:5e38\:6570\:ff0c\:5355\:4f4d\:ff1aF/m *)

(* \:5b9a\:4e49\:7279\:6027\:963b\:6297\:516c\:5f0f *)


(* \:7279\:6027\:963b\:6297\:516c\:5f0f *)
ZH1[f_] := 1.377*120*3.14/Sqrt[1-(c/(3.413*a*f*10^9))^2]

(* \:7ed8\:52363-5GHz\:9891\:6bb5\:7279\:6027\:963b\:6297\:66f2\:7ebf *)
Plot[ZH1[f]/1000, {f, 3, 5},  
 PlotRange -> All,
 AxesLabel -> {"Frequency (GHz)", "Impedance (k\[CapitalOmega])"}, 
 PlotLabel -> Style["\:5706\:67f1\:6ce2\:5bfc\:7279\:6027\:963b\:6297\:9891\:7387\:54cd\:5e94 (a=25mm)", 16, Bold],
 GridLines -> Automatic,
 PlotStyle -> {Thick, Blue}]


(* \:5b9a\:4e49\:771f\:7a7a\:4ecb\:8d28\:53c2\:6570 *)
c = 3*^8; (* \:5149\:901f\:ff0c\:5355\:4f4d\:ff1am/s *)
a = 22.86/1000; (* \:6ce2\:5bfc\:534a\:5f84\:ff0c\:5355\:4f4d\:ff1a\:7c73 *)
b = 10.16/1000; (* \:6ce2\:5bfc\:534a\:5f84\:ff0c\:5355\:4f4d\:ff1a\:7c73 *)
\[Mu] = 1; (* \:771f\:7a7a\:78c1\:5bfc\:7387\:ff0c\:5355\:4f4d\:ff1aH/m *)
\[CurlyEpsilon] = 1; (* \:771f\:7a7a\:4ecb\:7535\:5e38\:6570\:ff0c\:5355\:4f4d\:ff1aF/m *)

(* \:5b9a\:4e49\:7279\:6027\:963b\:6297\:516c\:5f0f *)


(* \:7279\:6027\:963b\:6297\:516c\:5f0f *)
ZH1[f_] := 1.571*b/a*120*Pi/Sqrt[1-(c/(2*a*f*10^9))^2]

(* \:7ed8\:52363-5GHz\:9891\:6bb5\:7279\:6027\:963b\:6297\:66f2\:7ebf *)
Plot[ZH1[f], {f, 8, 12},  
 PlotRange -> All,
 AxesLabel -> {"Frequency (GHz)", "Impedance (k\[CapitalOmega])"}, 
 PlotLabel -> Style["\:77e9\:5f62\:6ce2\:5bfc\:7279\:6027\:963b\:6297\:9891\:7387\:54cd\:5e94 (WR-90)", 16, Bold],
 GridLines -> Automatic,
 PlotStyle -> {Thick, Blue}]
