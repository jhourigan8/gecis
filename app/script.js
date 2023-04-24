var colors = ['blue', 'green', 'white', 'yellow', 'orange', 'red'],
		pieces = document.getElementsByClassName('piece');

// !!! Mine

// i and j are relative to this picture
// i is row, j is col
// geometry is hard!
//       4 4 4
//       4 4 4
//       4 4 4
// 0 0 0 2 2 2 1 1 1 3 3 3
// 0 0 0 2 2 2 1 1 1 3 3 3
// 0 0 0 2 2 2 1 1 1 3 3 3
//       5 5 5
//       5 5 5
//       5 5 5

var squares = Array(54)
function initSquares() {
	for (var f = 0; f < 6; f++) {
		for (var i = 0; i < 3; i++) {
			for (var j = 0; j < 3; j++) {
				squares[s(f,i,j)] = f;
			}
		}
	}
}
function isSolved() {
	for (var f = 0; f < 6; f++) {
		for (var i = 0; i < 3; i++) {
			for (var j = 0; j < 3; j++) {
				if (squares[s(f,i,j)] != f) { return false; }
			}
		}
	}
	return true;
}
function animateSequence(seq, count) {
	console.log(seq)
	++count
	document.getElementById("count").innerHTML = "Moves: " + count
	pair = seq.shift()
	animateRotation(pair[0], pair[1], Date.now())
	if (pair.length == 4) {
		animateRotation(pair[2], pair[3], Date.now())
	}
	if (seq.length == 0) { 
		solving = false 
	} else {
		new Promise(resolve => {
			setTimeout(resolve, 1000);
		}).then((res) => animateSequence(seq, count))
	}
}

var solving = false
async function solveCube(alg) {
	document.getElementById("solved").innerHTML = "Solving..."
	$.ajax({
		type: "POST",
		url: "http://localhost:5000/solve",
		data: { cube: JSON.stringify(squares), alg: JSON.stringify(alg) },
	}).then((data) => {
		if (solving) { return }
		document.getElementById("solved").innerHTML = "Solution:"
		solving = true
		console.log(data)
		if (data.response.length == 0) {
			document.getElementById("solved").innerHTML = "Solved!"
			return
		}
		animateSequence(data.response, 0)
	}, (data) => { // err same jank af lol
		if (solving) { return }
		console.log(JSON.parse(data.responseText))
		animateSequence(JSON.parse(data.responseText).response, 0)
	})
}
// brute force gang
function rotateSquares(f, cw) {
	var face_cycle = [s(f,0,0), s(f,0,1), s(f,0,2), s(f,1,2), s(f,2,2), s(f,2,1), s(f,2,0), s(f,1,0)]
	var outer_cycle = [] // top, left, bottom, right
	if (f == 0) {
		outer_cycle = [].concat(side(4, 1), side(2, 1), side(5, 1), side(3, 3))
	} else if (f == 1) {
		outer_cycle = [].concat(side(5, 3), side(2, 3), side(4, 3), side(3, 1))
	} else if (f == 2) {
		outer_cycle = [].concat(side(0, 3), side(4, 2), side(1, 1), side(5, 0))
	} else if (f == 3) {
		outer_cycle = [].concat(side(1, 3), side(4, 0), side(0, 1), side(5, 2))
	} else if (f == 4) {
		outer_cycle = [].concat(side(0, 0), side(3, 0), side(1, 0), side(2, 0))
	} else {
		outer_cycle = [].concat(side(2, 2), side(1, 2), side(3, 2), side(0, 2))
	}
	if (cw) {
		apply_move(face_cycle, 2)
		apply_move(outer_cycle, 3)
	} else {
		apply_move(face_cycle.reverse(), 2)
		apply_move(outer_cycle.reverse(), 3)
	}
	if (!solving) {
		document.getElementById("count").innerHTML = "Moves: 0"
	}
	if (isSolved()) {
		document.getElementById("solved").innerHTML = "Solved!"
	} else {
		document.getElementById("solved").innerHTML = ""
	}
	console.log("rotated " + f + ". cube: \n" + " " +
		"     " + " " + squares[s(4,0,0)] + " " + squares[s(4,0,1)] + " " + squares[s(4,0,2)] + " " + "\n" + " " +
		"     " + " " + squares[s(4,1,0)] + " " + squares[s(4,1,1)] + " " + squares[s(4,1,2)] + " " + "\n" + " " +
		"     " + " " + squares[s(4,2,0)] + " " + squares[s(4,2,1)] + " " + squares[s(4,2,2)] + " " + "\n" + " " +
		squares[s(0,0,0)] + " " + squares[s(0,0,1)] + " " + squares[s(0,0,2)] + " " + squares[s(2,0,0)] + " " + squares[s(2,0,1)] + " " + squares[s(2,0,2)] + " " + squares[s(1,0,0)] + " " + squares[s(1,0,1)] + " " + squares[s(1,0,2)] + " " + squares[s(3,0,0)] + " " + squares[s(3,0,1)] + " " + squares[s(3,0,2)] + " " + "\n" + " " +
		squares[s(0,1,0)] + " " + squares[s(0,1,1)] + " " + squares[s(0,1,2)] + " " + squares[s(2,1,0)] + " " + squares[s(2,1,1)] + " " + squares[s(2,1,2)] + " " + squares[s(1,1,0)] + " " + squares[s(1,1,1)] + " " + squares[s(1,1,2)] + " " + squares[s(3,1,0)] + " " + squares[s(3,1,1)] + " " + squares[s(3,1,2)] + " " + "\n" + " " +
		squares[s(0,2,0)] + " " + squares[s(0,2,1)] + " " + squares[s(0,2,2)] + " " + squares[s(2,2,0)] + " " + squares[s(2,2,1)] + " " + squares[s(2,2,2)] + " " + squares[s(1,2,0)] + " " + squares[s(1,2,1)] + " " + squares[s(1,2,2)] + " " + squares[s(3,2,0)] + " " + squares[s(3,2,1)] + " " + squares[s(3,2,2)] + " " + "\n" + " " +
		"     " + " " + squares[s(5,0,0)] + " " + squares[s(5,0,1)] + " " + squares[s(5,0,2)] + " " + "\n" + " " +
		"     " + " " + squares[s(5,1,0)] + " " + squares[s(5,1,1)] + " " + squares[s(5,1,2)] + " " + "\n" + " " +
		"     " + " " + squares[s(5,2,0)] + " " + squares[s(5,2,1)] + " " + squares[s(5,2,2)] + " " + "\n"
	)
}
// gives counter clockwise along side
// 0 is top, 1 is left, 2 is bottom, 3 is right
function side(f, n) {
	if (n == 0) { return [s(f, 0, 2), s(f, 0, 1), s(f, 0, 0)]}
	if (n == 1) { return [s(f, 0, 0), s(f, 1, 0), s(f, 2, 0)]}
	if (n == 2) { return [s(f, 2, 0), s(f, 2, 1), s(f, 2, 2)]}
	else { return [s(f, 2, 2), s(f, 1, 2), s(f, 0, 2)]}
}
// face, i, j to index
function s(f, i, j) {
	return 9*f + 3*i + j
}
function apply_move(cycle, amount) {
	for (var i = 0; i < amount; ++i) {
		cycle.push(cycle[i])
	}
	let tmp = [...squares]
	for (var i = 0; i < cycle.length - amount; ++i) {
		squares[cycle[i+amount]] = tmp[cycle[i]]
	}
}
// !!! Original

// Returns j-th adjacent face of i-th face
function mx(i, j) {
	return ([2, 4, 3, 5][j % 4 |0] + i % 2 * ((j|0) % 4 * 2 + 3) + 2 * (i / 2 |0)) % 6;
}

function getAxis(face) {
	return String.fromCharCode('X'.charCodeAt(0) + face / 2); // X, Y or Z
}

// Moves each of 26 pieces to their places, assigns IDs and attaches stickers
function assembleCube() {
	function moveto(face) {
		id = id + (1 << face);
		pieces[i].children[face].appendChild(document.createElement('div'))
			.setAttribute('class', 'sticker ' + colors[face]);
		return 'translate' + getAxis(face) + '(' + (face % 2 * 4 - 2) + 'em)';
	}
	initSquares()
	for (var id, x, i = 0; id = 0, i < 26; i++) {
		x = mx(i, i % 18);
		pieces[i].style.transform = 'rotateX(0deg)' + moveto(i % 6) +
			(i > 5 ? moveto(x) + (i > 17 ? moveto(mx(x, x + 2)) : '') : '');
		pieces[i].setAttribute('id', 'piece' + id);
	}
}

function getPieceBy(face, index, corner) {
	return document.getElementById('piece' +
		((1 << face) + (1 << mx(face, index)) + (1 << mx(face, index + 1)) * corner));
}

// Swaps stickers of the face (by clockwise) stated times, thereby rotates the face
function swapPieces(face, times) {
	for (var i = 0; i < 6 * times; i++) {
		var piece1 = getPieceBy(face, i / 2, i % 2),
				piece2 = getPieceBy(face, i / 2 + 1, i % 2);
		for (var j = 0; j < 5; j++) {
			var sticker1 = piece1.children[j < 4 ? mx(face, j) : face].firstChild,
					sticker2 = piece2.children[j < 4 ? mx(face, j + 1) : face].firstChild,
					className = sticker1 ? sticker1.className : '';
			if (className)
				sticker1.className = sticker2.className,
				sticker2.className = className;
		}
	}
}

// Animates rotation of the face (by clockwise if cw), and then swaps stickers
function animateRotation(face, cw, currentTime) {
	rotateSquares(face, cw);
	var k = .3 * (face % 2 * 2 - 1) * (2 * cw - 1),
			qubes = Array(9).fill(pieces[face]).map(function (value, index) {
				return index ? getPieceBy(face, index / 2, index % 2) : value;
			});
	(function rotatePieces() {
		var passed = Date.now() - currentTime,
				style = 'rotate' + getAxis(face) + '(' + k * passed * (passed < 300) + 'deg)';
		qubes.forEach(function (piece) {
			piece.style.transform = piece.style.transform.replace(/rotate.\(\S+\)/, style);
		});
		if (passed >= 300)
			return swapPieces(face, 3 - 2 * cw);
		requestAnimationFrame(rotatePieces);
	})();
}

// Events
function mousedown(md_e) {
	var startXY = pivot.style.transform.match(/-?\d+\.?\d*/g).map(Number),
			element = md_e.target.closest('.element'),
			face = [].indexOf.call((element || cube).parentNode.children, element);
	function mousemove(mm_e) {
		if (element) {
			var gid = /\d/.exec(document.elementFromPoint(mm_e.pageX, mm_e.pageY).id);
			if (gid && gid.input.includes('anchor')) {
				mouseup();
				var e = element.parentNode.children[mx(face, Number(gid) + 3)].hasChildNodes();
				animateRotation(mx(face, Number(gid) + 1 + 2 * e), e, Date.now());
			}
		} else pivot.style.transform =
			'rotateX(' + (startXY[0] - (mm_e.pageY - md_e.pageY) / 2) + 'deg)' +
			'rotateY(' + (startXY[1] + (mm_e.pageX - md_e.pageX) / 2) + 'deg)';
	}
	function mouseup() {
		document.body.appendChild(guide);
		scene.removeEventListener('mousemove', mousemove);
		document.removeEventListener('mouseup', mouseup);
		scene.addEventListener('mousedown', mousedown);
	}

	(element || document.body).appendChild(guide);
	scene.addEventListener('mousemove', mousemove);
	document.addEventListener('mouseup', mouseup);
	scene.removeEventListener('mousedown', mousedown);
}

document.ondragstart = function() { return false; }
window.addEventListener('load', assembleCube);
scene.addEventListener('mousedown', mousedown);