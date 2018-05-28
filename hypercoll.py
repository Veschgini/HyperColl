#!/usr/bin/env python
# -*- coding: utf-8 -*-

# HyperColl version 1.0 2018-04-06

# The software is provided under the terms of the \emph{zlib license}.
#
#
# Copyright \copyright\ 2017  Kambis Veschgini \& Manfred Salmhofer
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import math
import cairo


class HyperColl:
	'''We have developed a visually appealing representation for showing
	multiple shared connections between a large number of entities in a
	single 	graph. The library is in particular useful for visualizing
	collaborative projects.'''
	def __init__(self, labels,
				 filename="out.pdf", width = 595, height = 595
				 ):
		'''
		labels: A list of unique strings. They are used both to label the positions
		around the main diagram and to refere to these positions. The first label will
		be placed at zero angle (on the right hand side of the diagram).
		filename: Output file name.
		width, height: width and height of the page containing the diagram in points.
		A point is 1/72 inch or $0.3528$mm. The default value of 595pt coresponds to
		the width of A4 paper.
		'''
		self.labels = labels
		self.surface = cairo.PDFSurface(filename, width, height)
		self.context = cairo.Context(self.surface)
		self.context.translate(width/2,height/2)

	def hypercoll(self, colls, r, span, curvature,
		color_list=[[0.368417, 0.506779, 0.709798],	[0.880722, 0.611041, 0.142051],
					[0.560181, 0.691569, 0.194885],	[0.922526, 0.385626, 0.209179],
					[0.528488, 0.470624, 0.701351],	[0.772079, 0.431554, 0.102387],
					[0.363898, 0.618501, 0.782349],	[1, 0.75, 0], [0.647624,0.37816, 0.614037],
					[0.571589, 0.586483, 0.], [0.915, 0.3325, 0.2125],
					[0.400822, 0.522007, 0.85], [0.972829, 0.621644, 0.073362],
					[0.736783, 0.358, 0.503027], [0.280264, 0.715, 0.429209]],
					fill_opacity=0.3, edge_opacity=1.0, edge_width=1.0,
					labels=True,hspace=5,
					font_face = "Sans", font_slant=cairo.FONT_SLANT_NORMAL,font_weight=cairo.FONT_WEIGHT_BOLD,font_size=8,
					label_color=[1,1,1],label_opacity=1,background_color=[0.0392157, 0.101961, 0.27451],
					background_circle_color=[0.0392157, 0.101961, 0.27451],edge_order=None, background_disk=True,
					background_circle=True, background_circle_edge_width=1.0,fill=True):
		'''
		colls: A list of list of labels. Each list defines positions which will
		be connect using a hyperbolic patch. For example
		[['A','B','C'],['D','E']] will create two patches, the first one
		connecting A,B and C and the second one connecting D and E.
		r: the radius of the diagram including the labels in points.
		0<=span<=1: determines the span of the patch alongside the label. If a
		patch connects only two entities span must be larger than zero.
		0<=curvature<=1$: Determines the curvature of the edges connecting
		different labels.
		color_list: A list of colors used periodically to color the patches and
		their edges. The default values are taken from Wolfram Mathematica.
		We found them to work very well on a dark background.
		fill_opacity, edge_opacity: The opacity of the patch's filling and its
		edge.
		edge_order: A numeric list which sets the order in which the edges of
		the patches are drawn. For example edge_prder=[2,1] means that the edge
		of the second patch should be drawn first. By default the edges are
		drawn as if edge_order=[0,1,2,...,len(colls)-1]. The option is mostly
		relevant when two or more edges overlap.
		edge_width: Width of the edge in points.
		labels=True/False: If True, the labels are shown. If False, the labels
		still serve as a reference to the positions around the circle but the
		labels are not placed at those positions.
		hspace: Determines the extra space in points between the inner and out
		radius of the circular patches and both sides of the labels.
		font_face, font_slant, font_weight, font_size Parameter passed to Cairo
		for rendering the labels.
		label_color, label_opacity: Color of labels and their opacity.
		background_disk, background_color: When background_disk is set to True
		a disk with the color background_color is drawn in the background of
		the graphics.
		background_circle, background_circle_edge_width,
		background_circle_color: When background_circle is set to True a circle
		with the color background_circle_color and with of
		background_circle_edge_width is drawn around the main graphics.
		fill=True/False: If True the patches will be filled.
		'''

		if background_disk:
			self.disk(r, color=background_color)

		if background_circle:
			self.context.set_line_width(background_circle_edge_width);
			self.circle(r, color=background_circle_color)

		if labels:
			r = self.drawLabels(r,font_face=font_face,font_slant=font_slant,font_size=font_size,color=label_color,opacity=label_opacity,hspace=hspace)

		colls_index = [sorted([self.indexOfLabel(l) for l in c ]) for c in colls]
		if fill:
			j = -1
			for c in colls_index:
				j = (j + 1) % len(color_list)
				self.context.set_source_rgba(color_list[j][0], color_list[j][1], color_list[j][2], fill_opacity);
				self.patchPath(c, r, span, curvature)
				self.context.fill()
		j = -1
		self.context.set_line_width(edge_width);
		if (edge_order is None):
			edge_order = range(len(colls_index))

		for j in edge_order:
			c = colls_index[j]
			j = (j) % len(color_list)
			self.context.set_source_rgba(color_list[j][0], color_list[j][1], color_list[j][2], edge_opacity);
			self.patchPath(c, r, span, curvature)
			self.context.stroke()
		return r


	def sectors(self, r1, r2, dic, labels={}, font_face = "Sans",
	            font_slant=cairo.FONT_SLANT_NORMAL,
				font_weight=cairo.FONT_WEIGHT_BOLD, font_size=18,
				foreground_color=[1,1,1], opacity=1,
				background_color=[0.0392157, 0.101961, 0.27451],
				boundry_color=[1,1,1], boundy_width=1):
		'''
		r1,r2: inner and outer radius of the ring. The inner radius of the first
		ring is usually the same as the radius of the main diagram (parameter
		r provided to hypercoll).
		dic: A dictionary associating a property to every label the class was
		initialized with.
		labels: A dictionary giving each property defined in dic a label.
		If not empty, the labels are rendered in the corresponding sectors.
		font_face*,font_slant*,font_weight*,font_size* Parameter passed to Cairo
		for rendering the labels.
		foreground_color*, opacity*: Color and opacity used to render the labels
		associated to the properties from dic in the corresponding sectors.
		background_color*: Color used to fill the background of the sectors.
		boundry_color: The color used when rendering the dividing rules between
		sectors.
		boundry_with: The width of the dividing rules in points.
		* : Argument can be a single value or a dictionary
		'''
		n = len(self.labels);
		t = [dic[l] for l in self.labels]
		boundries=[]
		for k in range(0,len(t)):
			if t[(k-1)%len(t)]!=t[k]:
				boundries.append(k)

		select = lambda x,e: x[e] if isinstance(x,dict) else x

		for k in range(0,len(boundries)):
			a = boundries[k]
			b = (boundries[(k+1)%len(boundries)]-1) % len(self.labels)
			e = dic[self.labels[a]];

			if background_color is not None:
				d = 2.0*math.pi/n;
				co = select(background_color,e)
				self.context.set_source_rgba(co[0],co[1],co[2],1)
				# self.context.move_to(0.0 ,0.0);
				self.context.arc_negative(0, 0, r2, -(a-0.5)*d, -(b+0.5)*d)
				self.context.arc(0, 0, r1, -(b+0.5)*d, -(a-0.5)*d)
				self.context.fill()

			if labels is not None:
				l = labels.get(e,e)

				ffa = select(font_face,e)
				fsi = select(font_size,e)
				fsl = select(font_slant,e)
				co = select(foreground_color,e)
				op = select(opacity,e)

				self.context.set_source_rgba(co[0],co[1],co[2],op)
				self.sectorLabel(0.5*(r1+r2),a,b,l,font_face=ffa,font_size=fsi,font_slant=fsl)

			if boundry_color is not None and boundy_width>0:
				self.context.set_line_width(boundy_width)
				self.context.set_source_rgba(boundry_color[0],boundry_color[1],boundry_color[2],1)
				for b in boundries:
					phi = 2*math.pi/n*(b-0.5)
					self.context.move_to(r1*math.cos(phi),-r1*math.sin(phi))
					self.context.line_to(r2*math.cos(phi),-r2*math.sin(phi))
					self.context.stroke()

	def finish(self):
		self.surface.finish()

	def indexOfLabel(self,label):
		return self.labels.index(label)

	def disk(self, radius, color=[0.0392157, 0.101961, 0.27451], opacity=1.0):
		self.context.set_source_rgba (color[0], color[1], color[2], opacity);
		self.context.arc(0, 0, radius, 0, 2*math.pi);
		self.context.fill();

	def circle(self, radius, color=[1, 1, 1], opacity=1.0, line_width=1):
		self.context.set_source_rgba (color[0], color[1], color[2], opacity);
		self.context.set_line_width(line_width)
		self.context.arc(0, 0, radius, 0, 2*math.pi);
		self.context.stroke();


	@staticmethod
	def adjust_curvature(r, x, y, curvature):

		q = math.sqrt(x*x+y*y)/r
		c = max(-1, min(curvature*2-1, 0.9999))
		if (c>0):
			k = (q-c)/(1-c)
			k = max(k,0)
		else:
			k = -c + (1.0+c)*q
		return k*x/q , k*y/q

	@staticmethod
	def arc(radius, ax, ay, bx, by, cx ,cy, curvature):
		'''the function returns control points for drawing a cubic Bézier spline representing
		an arc centered at c=(center_x,cy), starting at a=(ax,ay) and ending at b=(bx,by).
		The function assumes |a-c|==|b-c|.
		radius: radius of inner disk
		0<=curvature<=1 :
			For curvature=0.5, the arc is approximatly circular.
			curvature>0.5 resutls in a difformation of the arc towars the origin=(0,0).'''

		r = math.sqrt((ax-cx)*(ax-cx) + (ay-cy)*(ay-cy))
		qx = bx - ax;
		qy = by - ay;
		px = ax + bx - 2*cx;
		py = ay + by - 2*cy;
		d = math.sqrt(px*px+py*py);
		if d < 1e-10:
			return ax,ay,bx,by
		t = 8.0/3.0*(r/d-0.5)*(-py/qx if abs(qx)>abs(qy) else px/qy);

		x1, y1 = HyperColl.adjust_curvature(radius,ax-t*(ay-cy), ay+t*(ax-cx), curvature)
		x2, y2 = HyperColl.adjust_curvature(radius,bx+t*(by-cy), by-t*(bx-cx), curvature)
		return x1, y1, x2, y2

	def	patchPath(self, elem, r, span, curvature):
		"""Draws the path connecting elements 'elem'"""
		n = len(self.labels)
		m = len(elem)
		a = 2*math.pi/n
		p_start = a*(elem[0]-span/2)
		self.context.scale(1,-1)
		self.context.move_to(r*math.cos(p_start),r*math.sin(p_start))
		for k in range(0,m):
			p1 = a*(elem[k]-span/2)
			p2 = a*(elem[k]+span/2)
			p3t = a*(elem[(k+1) % m]-span/2)
			p3 = p3t if p3t>p2 else p3t + 2.0*math.pi
			mid = 0.5*(p2+p3)
			t = abs(math.sin(0.5*(p3-p2)))
			q = r/math.sqrt(1-t*t)
			if (p3-p2>math.pi):
				mid = mid + math.pi
			self.context.arc(0.0,0.0,r,p1,p2)
			if(q<10000):
				x1, y1, x2 ,y2 = self.arc(r,r*math.cos(p2),r*math.sin(p2),r*math.cos(p3),r*math.sin(p3),q*math.cos(mid),q*math.sin(mid),curvature)
				self.context.curve_to(x1,y1,x2,y2,r*math.cos(p3),r*math.sin(p3))

			else:
				self.context.line_to(r*math.cos(p3),r*math.sin(p3))

		self.context.close_path()
		self.context.scale(1,-1)

	def	patchPath2(self, phi, r, curvature):
		"""Draws the path connecting elements 'elem'"""
		m = len(phi)
		p_start = phi[0][0];
		self.context.scale(1,-1)
		self.context.move_to(r*math.cos(p_start),r*math.sin(p_start))
		for k in range(0,m):
			p1 = phi[k][0]
			p2 = phi[k][1]
			p3t = phi[(k+1) % m][0]
			p3 = p3t if p3t>p2 else p3t + 2.0*math.pi
			mid = 0.5*(p2+p3)
			t = abs(math.sin(0.5*(p3-p2)))
			q = r/math.sqrt(1-t*t)
			if (p3-p2>math.pi):
				mid = mid + math.pi
			self.context.arc(0.0,0.0,r,p1,p2)
			if(q<10000):
				x1, y1, x2 ,y2 = self.arc(r,r*math.cos(p2),r*math.sin(p2),r*math.cos(p3),r*math.sin(p3),q*math.cos(mid),q*math.sin(mid),curvature)
				self.context.curve_to(x1,y1,x2,y2,r*math.cos(p3),r*math.sin(p3))

			else:
				self.context.line_to(r*math.cos(p3),r*math.sin(p3))

		self.context.close_path()
		self.context.scale(1,-1)

	def drawLabels(self,outer_radius, hspace = 5,
		font_face = "Sans", font_slant=cairo.FONT_SLANT_NORMAL,font_weight=cairo.FONT_WEIGHT_BOLD,font_size=8,
		color=[1,1,1],opacity=1):
		n = len(self.labels)
		max_width = 0.0;
		self.context.set_source_rgba(color[0],color[1],color[2],opacity)
		self.context.select_font_face(font_face,font_slant,font_weight)
		self.context.set_font_size(font_size)

		# measure the width of all labels
		for label in self.labels:
			x_bearing, y_bearing, width, height, x_advance, y_advance = self.context.text_extents(label);
			max_width = max(max_width, width)

		inner_radius = outer_radius - max_width - 2*hspace

		for k in range(0,len(self.labels)):
			label =  self.labels[k]
			phi = k*2.0*math.pi/n
			x_bearing, y_bearing, width, height, x_advance, y_advance = self.context.text_extents(label)
			matrix = self.context.get_matrix()
			self.context.rotate(-phi)
			if (phi>0.5*math.pi and phi<3.0/2.0*math.pi):
				self.context.translate(inner_radius+width+hspace, -0.5*height)
				self.context.scale(-1 ,-1)
			else:
				self.context.translate(inner_radius-x_bearing+hspace, 0.5*height)
			self.context.move_to(0.0 ,0.0)
			self.context.show_text(label)
			self.context.set_matrix(matrix)

		return inner_radius

	@staticmethod
	def trans(r, phi, flip, w, h, x, y):
		if (flip):
			u = (r+y+0.5*h) * math.cos((x-0.5*w)/r+phi)
			v = (r+y+0.5*h) * math.sin(-(x-0.5*w)/r-phi)
		else:
			u = (r-y-0.5*h) * math.cos((x-0.5*w)/r-phi)
			v = (r-y-0.5*h) * math.sin((x-0.5*w)/r-phi)
		return u, v

	def sectorLabel(self, r, a, b, label,font_face = "Sans", font_slant=cairo.FONT_SLANT_NORMAL,font_weight=cairo.FONT_WEIGHT_BOLD,font_size=8,
		color=[1,1,1],opacity=1):
		n = len(self.labels)
		phi = math.pi/n*(a+b)
		if a>b:
			phi = phi-math.pi
		self.context.select_font_face(font_face,font_slant,font_weight)
		self.context.set_font_size(font_size)

		# mod(mod(...)) -> positive modulo
		twopi = 2.0*math.pi
		flip = (((phi % twopi)+twopi) % twopi) >= math.pi

		x_bearing, y_bearing, w, h, x_advance, y_advance = self.context.text_extents(label);

		self.context.move_to(0,0)
		self.context.text_path(label)

		path = self.context.copy_path()
		self.context.new_path()

		for kind, points in path:
			if kind==cairo.PATH_MOVE_TO:
				x, y = points
				x, y = HyperColl.trans(r, phi, flip, w, h, x, y)
				self.context.move_to(x, y)
			elif kind==cairo.PATH_LINE_TO:
				x, y = points
				x, y = HyperColl.trans(r, phi, flip, w, h, x, y)
				self.context.line_to(x, y)
			elif kind==cairo.PATH_CURVE_TO:
				x1, y1, x2, y2, x3, y3 = points
				x1, y1 = HyperColl.trans(r, phi, flip, w, h, x1, y1)
				x2, y2 = HyperColl.trans(r, phi, flip, w, h, x2, y2)
				x3, y3 = HyperColl.trans(r, phi, flip, w, h, x3, y3)
				self.context.curve_to(x1, y1, x2, y2, x3, y3)
			elif kind==cairo.PATH_CLOSE_PATH:
			   self.context.close_path()
		self.context.fill()
