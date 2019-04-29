using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Diagnostics;
using Microsoft.CSharp;
using System.CodeDom.Compiler;
using System.Reflection;

public class ookp2
{
	public interface IScenario {
		IEnumerator<object> Scenario { get; }
		void OnReadCompleted(int bytes, bool error);
		void OnWriteCompleted(bool error);
		void OnClosed(bool error);
		void OnStopped(bool error);
		void OnSpawn(string info);
	}
	public interface IScenarioFactory {
		void init(string address);
		IScenario get_instance(string remote, byte[] ib, byte[] ob);
	}

	public enum OpType { Nop, Read, Write, Close, Exit, Spawn }

	public struct Op {
		public readonly OpType op;
		public readonly int arg;
		public Op(OpType op, int arg = 0) { this.op = op; this.arg = arg; }
	}

	internal class Backend {
		public string Address { get; private set; }
		public void Start(IScenarioFactory isf, int bsize = 65536) {
			TcpListener tl = new TcpListener(new IPEndPoint(IPAddress.Loopback, 0));
			tl.Start();
			Address = tl.LocalEndpoint.ToString();
			isf.init(Address);
			while (true) {
				var c = tl.AcceptTcpClient();
				c.LingerState.LingerTime = 0;
				c.LingerState.Enabled = true;
				var ns = c.GetStream();
				var ib = new byte[bsize];
				var ob = new byte[bsize];
				var sc = isf.get_instance(c.Client.RemoteEndPoint.ToString(), ib, ob);
				AsyncCallback cb = null;
				cb = ar => {
					if (ar != null) {
						switch (((Op)ar.AsyncState).op) {
							case OpType.Read: 
								int n = 0; bool ierror = false;
								try { n = ns.EndRead(ar); } catch (Exception) { ierror = true; }
								sc.OnReadCompleted(n, ierror); break;
							case OpType.Write:
								bool oerror = false;
								try { ns.EndWrite(ar); } catch (Exception) { oerror = true; }
								sc.OnWriteCompleted(oerror); break;
						}
					}
					if (sc.Scenario.MoveNext()) {
						Op op;
						if (sc.Scenario.Current is Op) op = (Op)sc.Scenario.Current; else op = new Op(OpType.Nop);
						switch (op.op) {
							case OpType.Nop: break;
							case OpType.Read: 
											 try { ns.BeginRead(ib, 0, (op.arg > 0) ? op.arg : ib.Length, cb, op); }
											 catch (Exception) { c.Close(); sc.OnClosed(true); } break;
							case OpType.Write: 
											 try { ns.BeginWrite(ob, 0, (op.arg > 0) ? op.arg : ob.Length, cb, op); }
											 catch (Exception) { c.Close(); sc.OnClosed(true); } break;
							case OpType.Close: c.Close(); sc.OnClosed(false); break;
							case OpType.Exit: Environment.Exit(0); break;
							case OpType.Spawn: 
											  var p = new Process();
											  p.StartInfo.FileName = Assembly.GetExecutingAssembly().Location;
											  try {
												  p.Start();
												  sc.OnSpawn(p.StandardOutput.ReadLine());
											  } catch (Exception) { }
											  break;
							default: c.Close(); sc.OnClosed(false); break;
						}
					}
				};
				cb(null);
			}
		}
	}

	internal class DefaultScenarioFactory : IScenarioFactory {
		private class ScenarioWriteAdapter : IScenario {
			private readonly IScenario InternalScenario;
			private readonly byte[] ob;
			private IEnumerator<object> TransformScenario() {
				while (InternalScenario.Scenario.MoveNext()) {
					if (InternalScenario.Scenario.Current is Op)
						yield return InternalScenario.Scenario.Current;
					else {
						using (var ms = new MemoryStream(Encoding.UTF8.GetBytes(InternalScenario.Scenario.Current.ToString()))) {
							int n = 0;
							while ((n = ms.Read(ob, 0, ob.Length)) > 0)
								yield return new Op(OpType.Write, n);
						}
					}
				}
			}
			public ScenarioWriteAdapter(IScenario sc, byte[] ob) {
				this.InternalScenario = sc; 
				this.ob = ob; 
				this.Scenario = TransformScenario();
			}
			public IEnumerator<object> Scenario { get; private set; }
			public void OnReadCompleted(int bytes, bool error) { InternalScenario.OnReadCompleted(bytes, error); }
			public void OnWriteCompleted(bool error) { InternalScenario.OnWriteCompleted(error); }
			public void OnClosed(bool error) { InternalScenario.OnClosed(error); }
			public void OnStopped(bool error) { InternalScenario.OnStopped(error); }
			public void OnSpawn(string info) { InternalScenario.OnSpawn(info); }
		}
		private readonly IScenarioFactory basefactory;
		public DefaultScenarioFactory(IScenarioFactory basefactory) { this.basefactory = basefactory; }
		public void init(string address) {
			Console.WriteLine(address); 
			this.basefactory.init(address);
		}
		public IScenario get_instance(string remote, byte[] ib, byte[] ob) {
			return new ScenarioWriteAdapter(basefactory.get_instance(remote, ib, ob), ob);
		}
	}

	public interface IContent { string ContentType { get; } }

	public class html : IContent {
		public class el {
			public readonly string tag;
			public readonly Dictionary<string, object> attr;
			public readonly List<object> text;
			public el(string tag, object[] attrvals = null, object[] txt = null) {
				this.tag = tag;
				this.attr = new Dictionary<string,object>();
				if (attrvals != null) {
					for (int i=0; i<attrvals.Length/2; i++)
						this.attr.Add((string)(attrvals[2*i]), attrvals[2*i+1]);
				}
				this.text = (txt == null) ? null : new List<object>(txt);
			}
			public override string ToString() {
				StringBuilder sb = new StringBuilder(string.Format("<{0}", tag));
				foreach (var a in attr) sb.Append(" ").Append(a.Key).Append("=\"").Append(a.Value.ToString().Replace("\"","\\\"")).Append("\"");
				sb.Append(">");
				if (text != null) {
					foreach (var o in text) sb.Append(o);
					sb.Append("</").Append(tag).Append(">");
				}
				return sb.ToString();
			}
		}
		public readonly object head;
		public readonly object body;
		public html(object head, object body) { 
			this.head = (head == null) ? "<head><meta http-equiv='content-type' content='text/html; charset=UTF-8'><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'></head>" : head;
			this.body = (body == null) ? "" : body;
		}
		public override string ToString() {
			return string.Format("<!DOCTYPE html><html>{0}{1}</html>\r\n", head, body);
		}
		public string ContentType { get { return "text/html"; } }
	}

	public class httpresp {
		public const string version = "1.1";
		public readonly int status;
		public readonly string reason;
		public readonly Dictionary<string,object> headers;
		public readonly object body;
		public httpresp(int status, string reason, object[] hdr, object body = null) {
			this.status = status;
			this.reason = (reason == null) ? "" : reason;
			headers = new Dictionary<string,object>();
			if (hdr != null) {
				for (int i=0; i<hdr.Length/2; i++)
					headers.Add((string)hdr[2*i], hdr[2*i+1]);
			}
			this.body = body;
		}
		public httpresp(object body, string ct = null) {
			this.status = 200;
			this.reason = "OK";
			this.headers = new Dictionary<string, object>();
			if (ct == null && body is IContent)
				this.headers.Add("Content-Type", ((IContent)body).ContentType);
			else if (ct != null)
				this.headers.Add("Content-Type", ct);
			this.headers.Add("Connection", "close");
			this.body = body;
		}
		public override string ToString() {
			StringBuilder sb = new StringBuilder(string.Format("HTTP/{0} {1} {2}\r\n", version, status, reason));
			foreach (var h in headers) sb.Append(h.Key).Append(": ").Append(h.Value).Append("\r\n");
			sb.Append("\r\n");
			if (body != null) sb.Append(body.ToString());
			return sb.ToString();
		}
	}

	public class InitialScenarioFactory : IScenarioFactory {
		public class scenario : IScenario {
			const int MAXCHECK = 10;
			const string CODE = "4Gm(xx*0 0 -0!0#*91/?1)m)";
			private static readonly string welcome_page;
			protected readonly InterpState st;
			protected class InterpState {
				public const int SZ = 65536;
				public readonly string local;
				public readonly string remote;
				public readonly byte[] ib;
				public readonly byte[] ob;
				public int bytes_available;
				public string spawn_info;
				public StringBuilder codesb;
				public dynamic[] d;
				public dynamic[] m;
				public InterpState(string local, string remote, byte[] ib, byte[] ob) {
					this.local = local; this.remote = remote; this.ib = ib; this.ob = ob;
					this.d = new object[SZ];
					this.m = new object[SZ];
					this.codesb = new StringBuilder("");
				}
				public object Evolve(string p, double x, string s, int i = 0, ushort t = SZ-1) {
					int ibidx = 0, obidx = 0;
					for (; ; i++) {
						switch (s[i]) {
							case 'x': d[--t] = x; break;
							case ' ': t++; break;
							case '+': d[t+1] = (double)d[t] + (double)d[++t]; break;
							case '-': d[t+1] = (double)d[t] - (double)d[++t]; break;
							case '*': d[t+1] = (double)d[t] * (double)d[++t]; break;
							case '/': d[t+1] = (double)d[t] / (double)d[++t]; break;
							case '^': d[t] = Math.Sqrt((double)d[t]); break;
							case '!': m[(int)d[t++]] = d[t]; break;
							case '#': d[t] = m[(int)d[t]]; break;
							case '(': var y = Evolve(p, (double)(d[t++]), s, (int)d[t++], t); d[--t] = y; break;
							case ')': return d[t++];
							case '?': if (double.IsNaN((double)d[t]) || double.IsNaN((double)d[t+1]) || 
											  double.IsInfinity((double)d[t]) || double.IsInfinity((double)d[t+1]))
										  return null;
									  else if ((double)d[t++] <= (double)d[t++]) i += (int)d[t++]; else t++; break;
							case 'm': d[--t] = new InterpState(local, remote, ib, ob).Evolve(p, x, p); break;
							case 'y': return new Op((OpType)((int)(d[t])), (int)(d[t+1]));
							case 'Y': return new Op((OpType)((int)(d[t])));
							case 'I': ibidx = (int)d[t]; break;
							case 'i': d[t] = ib[ibidx++]; break;
							case 'O': obidx = (int)d[t]; break;
							case 'o': ob[obidx++] = (byte)d[t]; break;
							case 'c': codesb.Append((char)(d[t])); break;
							case 'r': codesb.Clear(); break;
							case 'l': Console.Write((char)(d[t])); break;
							case 'C': try {
										  int n = (int)d[t];
										  var csc = new CSharpCodeProvider();
										  var par = new CompilerParameters(new[] { "mscorlib.dll", "System.Core.dll", "Microsoft.CSharp.dll", Assembly.GetExecutingAssembly().Location }, "extension" + n.ToString(), false);
										  par.GenerateInMemory = true;
										  par.GenerateExecutable = false;
										  CompilerResults res = csc.CompileAssemblyFromSource(par, codesb.ToString());
										  if (res.Errors.Count == 0) {
											  dynamic o = res.CompiledAssembly.CreateInstance("ext" + n.ToString());
											  o.init(this);
											  Console.WriteLine("{0} : {1} : Extension {2} : Loaded", DateTime.Now, remote, n);
										  } else
											  Console.WriteLine("{0} : {1} : Extension {2} : Error ({3})", DateTime.Now, remote, n, res.Errors[0]);
									  } catch (Exception e) { Console.WriteLine(e.ToString()); } break;
							default: d[--t] = (double)(s[i] - '0'); break;
						}
					}
				}
			}

			private IEnumerator<object> make_scenario() {
				yield return new Op(OpType.Read);
				if (st.bytes_available > 0) {
					if (st.spawn_info != null) {
						yield return new httpresp(302, "Found", new object[] { "Location", "http://" + st.spawn_info, "Connection", "close" });
						yield return new Op(OpType.Close);
					} else {
						using (var sr = new StreamReader(new MemoryStream(st.ib), Encoding.UTF8)) {
							var s = sr.ReadLine();
							var i = s.IndexOf('?');
							if (i >= 0) {
								var code = Uri.UnescapeDataString(s.Substring(i+1));
								var success = true;
								try {
									for (int k = 1; k <= MAXCHECK; k++)
										st.Evolve(code, k, CODE);
								} catch (Exception) {
									success = false;
									Console.WriteLine("{0} : {1} : Cheating alert", DateTime.Now, st.remote);
								}
								if (success) {
									for (var o = st.Evolve(null, 0, code); o != null && o is Op; o = st.Evolve(null, 0, code))
										yield return o;
								} else {
									yield return new httpresp(400, "", new object[] { "Connection", "close" });
									yield return new Op(OpType.Close);
								}
							} else {
								yield return new httpresp(welcome_page, "text/html");
								yield return new Op(OpType.Close);
							}
						}
					}
				} else
					yield return new Op(OpType.Close);
			}
			static scenario() {
				welcome_page = new html(
						new html.el("head", null, new object[] { 
							new html.el("meta", new object[] {"http-equiv", "content-type", "content", "text/html; charset=UTF-8"}),
							new html.el("meta", new object[] {"charset", "utf-8"}),
							new html.el("style", null, new object[] {"@keyframes drop {0% {opacity: 0;} 5% {opacity: 1;} 17% {opacity: 1;transform: rotate(0deg); } 19% {opacity: 1;transform: rotate(97deg); } 21% {opacity: 1;transform: rotate(85deg); } 22% {opacity: 1;transform: translateY(84px) rotate(82deg); } 25% {opacity: 0;transform: translateY(171px) rotate(81deg); } 80% {opacity: 0;} 100% {opacity: 0;}}"})
							}),
						new html.el("body", null, new object[] {
							new html.el("h1", new object[] {"style", "font-family:'Arial Narrow'"}, new object[] { "Welcome to OOKP " + new html.el("font", new object[] {"color", "red"}, new object[] {"Module 2"}) + "!" }),
							new html.el("br"),
							"Enter your code " + new html.el("div", new object[] { "style", "display:inline;transform-origin:10% 75%;animation:drop 20s;" }, new object[] {"below"}),
							new html.el("br"),
							new html.el("textarea", new object[] {"id", "scenario", "cols", "40", "rows", "15"}, new object[] {}),
							new html.el("br"),
							new html.el("button", new object[] {"onclick", 
									"window.location.href='/?'+encodeURIComponent(document.getElementById('scenario').value)"}, 
									new object[] {"Submit"}) 
							})).ToString();
			}
			public scenario(string local, string remote, byte[] ib, byte[] ob) {
				this.st = new InterpState(local, remote, ib, ob);
				this.Scenario = make_scenario();
			}
			public IEnumerator<object> Scenario { get; private set; }
			public virtual void OnReadCompleted(int bytes, bool error) { st.bytes_available = (error)?0:bytes; }
			public virtual void OnWriteCompleted(bool error) {  }
			public virtual void OnClosed(bool error) { }
			public virtual void OnStopped(bool error) {  }
			public virtual void OnSpawn(string info) { st.spawn_info = info; }
		}
		private string local;
		public void init(string address) { this.local = address; }
		public IScenario get_instance(string remote, byte[] ib, byte[] ob) {
			return new scenario(local, remote, ib, ob);
		}
	}

	static void Main(string[] args)
	{
		new Backend().Start(new DefaultScenarioFactory(new InitialScenarioFactory()));
	}
}
