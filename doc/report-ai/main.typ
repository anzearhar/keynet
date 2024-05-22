#import "@preview/cetz:0.2.2"

#let accent_color = cmyk(0%, 94%, 94%, 6%)

#set document(title: "Project report", author: "Arhar, Kostanjšek, Ločičnik", date: datetime.today())
#set page(
    numbering: "1",
    header: locate(loc => {
        set text(fill: luma(120))
        if counter(page).at(loc).first() > 1 [#h(1fr)KeyNet #h(2mm) --- #h(2mm) #counter(page).display("1/1", both: true)]
        }),
    footer: [],
    header-ascent: 25%
)

#set text(font: "Source Sans Pro", weight: "light", size: 9pt)
#set par(justify: true, leading: .55em, first-line-indent: 1.8em)

#show par: set block(spacing: 0.55em)
#show heading: set block(above: 1.4em, below: .5em)
#show ref: set text(fill: accent_color)
#show footnote: set text(fill: accent_color)

#set table(stroke: none)
#set table.hline(stroke: .15mm + black)
#set table.vline(stroke: .15mm + black)
#set footnote.entry(separator: line(length: 30%, stroke: .15mm))

#align(right)[
    #set text(fill: luma(120))
    FRI Artificial intelligence course 2023\
    Project report
]

#v(1em)
#text(fill: luma(120), size: 10pt)[
    #heading()[
        #set text(weight: "regular")
        KeyNet: keyboard layout optimization using network analysis and genetic algorithms
    ]
    Anže Arhar, Kristjan Kostanjšek, and Nejc Ločičnik
]
#v(3em)

// #set text(font: "New Computer Modern")
#set heading(numbering: "1.1")
#show heading: set text(fill: luma(120), weight: "semibold")
#show heading: set block(above: 1.4em, below: .8em)
#show: columns.with(2)

= Introduction

#lorem(100)

= Methods

#lorem(50)

== Network analysis

#lorem(200)

== Genetic algorithms

#lorem(200)

#let img_width = 25mm
#figure(
    caption: [Matrices],
    grid(
        columns: 3,
        row-gutter: (1mm, 3mm, 1mm, 3mm),
        gutter: .4mm,
        image("./img/p.png", width: img_width),
        image("./img/pi.png", width: img_width),
        image("./img/d.png", width: img_width),
        [$P$], [$pi$], [$D$],
        image("./img/r.png", width: img_width),
        image("./img/f.png", width: img_width),
        image("./img/e.png", width: img_width),
        [$R$], [$F$], [$E$]
    )
)

== Evaluation

#lorem(200)

= Results

#lorem(200)

= Discussion

#lorem(100)

#bibliography("refs.yml")
