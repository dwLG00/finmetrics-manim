from manim import *
import math
import random

BASEGRAPH = Axes(
	x_range=[0, 10, 1],
	y_range=[0, 10, 1],
	tips=False
)
'''
BASEGRAPH.get_axes()[0].add_labels({
	1: MathTex("t_1"),
	2: MathTex("t_2"),
	3: MathTex("t_3"),
	4: MathTex("t_4"),
	5: MathTex("t_5"),
	6: MathTex("t_6"),
	7: MathTex("t_7"),
	8: MathTex("t_8"),
	9: MathTex("t_9"),
	10: MathTex("t_10")
})
'''
new_label_group = VGroup(
	MathTex("t_1"),
	MathTex("t_2"),
	MathTex("t_3"),
	MathTex("t_4"),
	MathTex("t_5"),
	MathTex("t_6"),
	MathTex("t_7"),
	MathTex("t_8"),
	MathTex("t_9"),
	MathTex("t_10")
)
BASEGRAPH.get_axes()[0].labels = new_label_group

scatter_values = [ #TODO temp values, actually add in the values
	(0, 4),
	(1, 3),
	(2, 4),
	(3, 5),
	(4, 4),
	(5, 5),
	(6, 4),
	(7, 3),
	(8, 4),
	(9, 5),
]
scatter_x = [point[0] for point in scatter_values]
scatter_y = [point[1] for point in scatter_values]

ax = BASEGRAPH.add_coordinates()
scatter_dots = [
	Dot(ax.coords_to_point(*point), color=WHITE) for point in scatter_values
]
SCATTERDOTS = VGroup(*scatter_dots)
line_graph = [
	Line(
		start=BASEGRAPH.coords_to_point(*scatter_values[i]),
		end=BASEGRAPH.coords_to_point(*scatter_values[i+1]),
		color=WHITE
	) for i in range(len(scatter_dots)-1)
]
LINEGRAPH = VGroup(*line_graph)
WHOLEGRAPH = VGroup(BASEGRAPH, SCATTERDOTS, LINEGRAPH)
WHOLEGRAPH.scale(0.7)

def set_line_graph_color(line_graph, scatter_values, animate=False):
	if not animate:
		for i in range(len(line_graph)):
			if scatter_values[i+1][1] > scatter_values[i][1]:
				line_graph[i].set_color(GREEN)
			elif scatter_values[i+1][1] < scatter_values[i][1]:
				line_graph[i].set_color(RED)
	else:
		animations = []
		for i in range(len(line_graph)):
			if scatter_values[i+1][1] > scatter_values[i][1]:
				animations.append(line_graph[i].animate.set_color(GREEN))
			elif scatter_values[i+1][1] < scatter_values[i][1]:
				animations.append(line_graph[i].animate.set_color(RED))
		return animations

class RandomWalkDisplay(Scene):
	def construct(self):
		self.play(Create(BASEGRAPH))
		self.wait(2)
		self.play(Create(SCATTERDOTS))
		self.wait(2)

		eq = MathTex("P_{t+1}", "=", "P_{t}", "+", "\epsilon", "+", "\mu")
		eq.next_to(BASEGRAPH, DOWN)
		self.play(Create(eq))
		self.wait(2)

		#self.play(Create(LINEGRAPH))
		#self.wait(2)

		eq2 = MathTex("E(t)", "=", "\mu t")
		eq2.move_to(eq)
		eq.target = eq2
		self.play(MoveToTarget(eq))
		self.wait(2)

		question_mark = MathTex("?")
		question_mark.scale(5)
		question_mark.set_color(RED)
		self.play(FadeIn(question_mark))
		self.wait(2)
		self.play(FadeOut(question_mark), FadeOut(eq))
		self.wait(2)

		coloring_animations = set_line_graph_color(line_graph, scatter_values, animate=True)
		self.play(Create(LINEGRAPH))
		self.wait(1)
		self.play(*coloring_animations)
		self.wait(1)

		labels = [
			MathTex("e^", "{r_1}"),
			MathTex("e^", "{r_2}"),
			MathTex("e^", "{r_3}"),
			MathTex("e^", "{r_4}"),
			MathTex("e^", "{r_5}"),
			MathTex("e^", "{r_6}"),
			MathTex("e^", "{r_7}"),
			MathTex("e^", "{r_8}"),
			MathTex("e^", "{r_9}"),
		]
		for i, label in enumerate(labels):
			label.scale(0.7)
			if scatter_values[i+1][1] > scatter_values[i][1]:
				label[1].set_color(GREEN)
			elif scatter_values[i+1][1] < scatter_values[i][1]:
				label[1].set_color(RED)
			label.next_to(line_graph[i], UP*0.5)
		line_labels = VGroup(*labels)

		eq3 = MathTex("P(t+1)", "=", "e^{r_t}", "P(t)")
		eq3.move_to(eq2)
		eq2.target = eq3

		self.play(FadeIn(line_labels), MoveToTarget(eq2))
		self.wait(2)
		eq2.set_opacity(0)

		everything = Group(WHOLEGRAPH, line_labels, eq3)
		exp = MathTex("\{",
			"r_1,\,",
			"r_2,\,",
			"r_3,\,",
			"r_4,\,",
			"r_5,\,",
			"r_6,\,",
			"r_7,\,",
			"r_8,\,",
			"r_9",
		"\}")

		self.play(Write(exp), FadeOut(everything))
		self.wait(2)

		eq4 = MathTex(r"r_{normal,i} = \frac{r_{i} - \tilde{r}}{\sigma_r}")
		eq4.move_to(exp)

		self.play(exp.animate.shift(UP), Write(eq4))


class FirstOrderAutocorrelationCoefficient(Scene):
	def construct(self):
		text = Tex("First Order Autocorrelation Coefficient")
		text.scale(1.5)
		self.play(Write(text))
		self.wait(2)

class RhoDemonstration(Scene):
	def construct(self):
		graph = Axes(
			x_range=[0, 10, 1],
			y_range=[-3, 3, 1],
			tips=False
		)
		scatter_values = [
			(0, 0),
			(1, -1.23),
			(2, 1.04),
			(3, 0.78),
			(4, -0.98),
			(5, 0.78),
			(6, -0.98),
			(7, -1.23),
			(8, 1.03),
			(9, 0.78)
		]
		ax = graph.add_coordinates()
		scatter_dots = [
			Dot(ax.coords_to_point(*point), color=WHITE) for point in scatter_values
		]
		dots_group = VGroup(*scatter_dots)
		lines = [
			Line(start=ax.coords_to_point(*scatter_values[i]), end=ax.coords_to_point(*scatter_values[i+1])) for i in range(len(scatter_dots) - 1)
		]
		lines_group = VGroup(*lines)
		set_line_graph_color(lines_group, scatter_values)
		self.play(Create(graph), Create(dots_group), Create(lines_group))
		self.wait(2)

		all = Group(graph, dots_group, lines_group)
		self.play(FadeOut(all))
		self.wait(2)

		high_rho_graph = Axes(
			x_range=[0, 20, 1],
			y_range=[-3, 3, 0.5],
			tips=False
		)
		f = lambda x: math.sin(x * math.pi / 3.5)
		scatter_values = [(x, f(x)) for x in range(20)]
		ax2 = high_rho_graph.add_coordinates()
		scatter_dots = [Dot(ax2.coords_to_point(*point), color=WHITE) for point in scatter_values]
		lines = [
			Line(start=ax2.coords_to_point(*scatter_values[i]), end=ax2.coords_to_point(*scatter_values[i+1])) for i in range(len(scatter_dots) - 1)
		]
		scatter_group = VGroup(*scatter_dots)
		lines_group = VGroup(*lines)
		set_line_graph_color(lines_group, scatter_values)
		self.play(Create(high_rho_graph), Create(scatter_group), Create(lines_group))
		self.wait(2)

		all = Group(high_rho_graph, scatter_group, lines_group)
		exp = MathTex(r"\rho \approx 1.0")
		exp.next_to(high_rho_graph, DOWN)
		exp.shift(UP*1.5)

		self.play(Write(exp))
		self.wait(2)

		self.play(FadeOut(all), FadeOut(exp))
		self.wait(2)

		low_rho_graph = Axes(
			x_range=[0, 20, 1],
			y_range=[-3, 3, 0.5],
			tips=False
		)
		ax3 = low_rho_graph.add_coordinates()
		f = lambda x: (-1)**x * x / 10
		scatter_values = [(x, f(x)) for x in range(20)]
		scatter_dots = [Dot(ax3.coords_to_point(*point), color=WHITE) for point in scatter_values]
		scatter_lines = [
			Line(start=ax2.coords_to_point(*scatter_values[i]), end=ax2.coords_to_point(*scatter_values[i+1])) for i in range(len(scatter_dots) - 1)
		]
		dots_group = VGroup(*scatter_dots)
		lines_group = VGroup(*scatter_lines)
		set_line_graph_color(lines_group, scatter_values)
		self.play(Create(low_rho_graph), Create(dots_group), Create(lines_group))
		self.wait(2)

		exp = MathTex(r"\rho \approx -1.0")
		exp.next_to(low_rho_graph, DOWN)
		exp.shift(UP*1.5)
		self.play(Write(exp))
		self.wait(2)

		all = Group(low_rho_graph, dots_group, lines_group)
		self.play(FadeOut(all), FadeOut(exp))
		self.wait(2)

		rw_graph = Axes(
			x_range=[0, 20, 1],
			y_range=[-3, 3, 0.5],
			tips=False
		)
		ax4 = rw_graph.add_coordinates()

		scatter_values = []
		random_values = [0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0]
		for i in range(20):
			if i == 0:
				scatter_values.append((0, 0))
			else:
				scatter_values.append((i, scatter_values[-1][1] + (random_values[i-1] - 0.5)*0.5))

		scatter_dots = [Dot(ax4.coords_to_point(*point), color=WHITE) for point in scatter_values]
		scatter_lines = [
			Line(start=ax4.coords_to_point(*scatter_values[i]), end=ax4.coords_to_point(*scatter_values[i+1])) for i in range(len(scatter_dots) - 1)
		]
		dots_group = VGroup(*scatter_dots)
		lines_group = VGroup(*scatter_lines)
		set_line_graph_color(lines_group, scatter_values)
		self.play(Create(rw_graph), Create(dots_group), Create(lines_group))
		self.wait(2)

		exp = MathTex(r"\rho \approx 0")
		exp.next_to(rw_graph, DOWN)
		exp.shift(UP*1.5)
		self.play(Write(exp))
		self.wait(2)

		arrow = Arrow(start=UP, end=DOWN+UP)

		all = Group(rw_graph, dots_group, lines_group)
		self.play(FadeOut(all), exp.animate.shift(UP * 4))
		self.wait(1)
		arrow.next_to(exp, DOWN)
		self.play(FadeIn(arrow))
		self.wait(1)
		text = Tex("Series follows Random Walk")
		text.next_to(arrow, DOWN)
		self.play(Write(text))
		self.wait(2)
		self.play(FadeOut(exp), FadeOut(arrow), FadeOut(text))
		self.wait(2)

class Intro(Scene):
	def construct(self):
		text = Tex("Stock Prices and Random Walk Modeling")
		text2 = Tex("Dylan, Jack, Deshan")
		text.scale(1.5)
		text.shift(UP*0.5)
		text2.next_to(text, DOWN)
		text3 = Tex("(Presentation by Dylan)")
		text3.scale(0.5)
		text3.next_to(text2, DOWN)
		self.play(Write(text), Write(text2))
		self.wait(2)
		self.play(Write(text3))
		self.wait(1)
		self.play(FadeOut(text), FadeOut(text2), FadeOut(text3))
		self.wait(1)
