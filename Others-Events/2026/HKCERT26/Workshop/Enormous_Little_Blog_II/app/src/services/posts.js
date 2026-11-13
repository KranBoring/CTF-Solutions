const posts = [{
  id: 3,
  author: 'admin',
  private: true,
  title: `Our Team Flag`,
  content: `We are now buddies. Here we share our flag of glory: <code>${process.env.FLAG}</code>.`,
  publishedAt: '2022-10-08 14:30:00'
}, {
  id: 2,
  author: 'admin',
  private: false,
  title: 'What is Capture the Flag?',
  content: `<p>Capture the Flag (CTF) is a special kind of information security competitions. There are three common types of CTFs: Jeopardy, Attack-Defence and mixed.</p>
<p>Jeopardy-style CTFs has a couple of questions (tasks) in range of categories. For example, Web, Forensic, Crypto, Binary or something else. Team can gain some points for every solved task. More points for more complicated tasks usually. The next task in chain can be opened only after some team solve previous task. Then the game time is over sum of points shows you a CTF winer. Famous example of such CTF is Defcon CTF quals.</p>
<p>Well, attack-defence is another interesting kind of competitions. Here every team has own network(or only one host) with vulnarable services. Your team has time for patching your services and developing exploits usually. So, then organizers connects participants of competition and the wargame starts! You should protect own services for defence points and hack opponents for attack points. Historically this is a first type of CTFs, everybody knows about DEF CON CTF - something like a World Cup of all other competitions.</p>
<p>Mixed competitions may vary possible formats. It may be something like wargame with special time for task-based elements (e.g. UCSB iCTF).</p>
<p>CTF games often touch on many other aspects of information security: cryptography, stego, binary analysis, reverse engeneering, mobile security and others. Good teams generally have strong skills and experience in all these issues.</p>`,
  publishedAt: '2020-01-01 08:00:00'
}, {
  id: 1,
  author: 'admin',
  private: false,
  title: 'Blog Template',
  content: `<h2>Heading</h2>
<h3>Sub-heading</h3>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus elementum turpis at nunc tempor elementum.</p>
<ul>
    <li>Point 1</li>
    <li>Point 2</li>
    <li>Point 3</li>
</ul>
<h3>Sub-heading</h3>
<blockquote>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus elementum turpis at nunc tempor elementum. Nullam placerat nunc ligula, id placerat ipsum dignissim nec. Aliquam erat volutpat. Maecenas quis est nibh. Phasellus porta eget tellus tincidunt iaculis. Aliquam molestie gravida consequat. Donec viverra felis ut elit aliquet varius.</blockquote>
<h3>Sub-heading</h3>
<pre>
    <code>
from pwn import *
context(arch = 'i386', os = 'linux')

r = remote('exploitme.example.com', 31337)
r.send(asm(hellcraft.sh()))
r.interactive()
    </code>
</pre>`,
  publishedAt: '2020-01-01 08:00:00'
}]

function getPosts () {
  return posts
}

module.exports = {
  getPosts
}
