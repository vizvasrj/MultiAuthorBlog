/*
 * AutoSuggest
 * Copyright 2009-2010 Drew Wilson
 * www.drewwilson.com
 * code.drewwilson.com/entry/autosuggest-jquery-plugin
 *
 * Forked by Wu Yuntao
 * github.com/wuyuntao/jquery-autosuggest
 *
 * Version 1.6.2
 *
 * This Plug-In will auto-complete or auto-suggest completed search queries
 * for you as you type. You can add multiple selections and remove them on
 * the fly. It supports keybord navigation (UP + DOWN + RETURN), as well
 * as multiple AutoSuggest fields on the same page.
 *
 * Inspired by the Autocomplete plugin by: Joern Zaefferer
 * and the Facelist plugin by: Ian Tearle (iantearle.com)
 *
 * This AutoSuggest jQuery plug-in is dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 */
(function (a) {
    a.fn.autoSuggest = function (h, e) {
        var i = {
            asHtmlID: false,
            startText: "Enter Name Here",
            usePlaceholder: false,
            emptyText: "No Results Found",
            preFill: {},
            limitText: "No More Selections Are Allowed",
            selectedItemProp: "value",
            selectedValuesProp: "value",
            searchObjProps: "value",
            queryParam: "q",
            retrieveLimit: false,
            extraParams: "",
            matchCase: false,
            minChars: 1,
            keyDelay: 400,
            resultsHighlight: true,
            neverSubmit: false,
            selectionLimit: false,
            showResultList: true,
            showResultListWhenNoMatch: false,
            canGenerateNewSelections: true,
            start: function () {},
            selectionClick: function (j) {},
            selectionAdded: function (j) {},
            selectionRemoved: function (j) {
                j.remove()
            },
            formatList: false,
            beforeRetrieve: function (j) {
                return j
            },
            retrieveComplete: function (j) {
                return j
            },
            resultClick: function (j) {},
            resultsComplete: function () {}
        };
        var g = a.extend(i, e);

        function d(j) {
            var l = 0;
            for (k in j) {
                if (j.hasOwnProperty(k)) {
                    l++
                }
            }
            return l
        }

        function c() {
            var j = g.extraParams;
            if (a.isFunction(j)) {
                return j()
            }
            return j
        }
        var b;
        var f = null;
        if (typeof h == "function") {
            b = h
        } else {
            if (typeof h == "string") {
                b = function (m, l) {
                    var j = "";
                    if (g.retrieveLimit) {
                        j = "&limit=" + encodeURIComponent(g.retrieveLimit)
                    }
                    f = a.getJSON(h + "?" + g.queryParam + "=" + encodeURIComponent(m) + j + c(), function (o) {
                        var n = g.retrieveComplete.call(this, o);
                        l(n, m)
                    })
                }
            } else {
                if (typeof h == "object" && d(h) > 0) {
                    b = function (l, j) {
                        j(h, l)
                    }
                }
            }
        }
        if (b) {
            return this.each(function (z) {
                if (!g.asHtmlID) {
                    z = z + "" + Math.floor(Math.random() * 100);
                    var m = "as-input-" + z
                } else {
                    z = g.asHtmlID;
                    var m = z
                }
                g.start.call(this, {
                    add: function (x) {
                        K(x, "u" + a("li", G).length).addClass("blur")
                    },
                    remove: function (x) {
                        M.val(M.val().replace("," + x + ",", ","));
                        G.find('li[data-value = "' + x + '"]').remove()
                    }
                });
                var B = a(this);
                B.attr("autocomplete", "off").addClass("as-input").attr("id", m);
                if (g.usePlaceholder) {
                    B.attr("placeholder", g.startText)
                } else {
                    B.val(g.startText)
                }
                var F = false;
                B.wrap('<ul class="as-selections" id="as-selections-' + z + '"></ul>').wrap('<li class="as-original" id="as-original-' + z + '"></li>');
                var G = a("#as-selections-" + z);
                var v = a("#as-original-" + z);
                var o = a('<div class="as-results" id="as-results-' + z + '"></div>').hide();
                var p = a('<ul class="as-list"></ul>');
                var M = a('<input type="hidden" class="as-values" name="as_values_' + z + '" id="as-values-' + z + '" />');
                var u = "";
                if (typeof g.preFill == "string") {
                    var C = g.preFill.split(",");
                    for (var I = 0; I < C.length; I++) {
                        var n = {};
                        n[g.selectedValuesProp] = C[I];
                        if (C[I] != "") {
                            K(n, "000" + I)
                        }
                    }
                    u = g.preFill
                } else {
                    u = "";
                    var N = 0;
                    for (k in g.preFill) {
                        if (g.preFill.hasOwnProperty(k)) {
                            N++
                        }
                    }
                    if (N > 0) {
                        for (var I = 0; I < N; I++) {
                            var D = g.preFill[I][g.selectedValuesProp];
                            if (D == undefined) {
                                D = ""
                            }
                            u = u + D + ",";
                            if (D != "") {
                                K(g.preFill[I], "000" + I)
                            }
                        }
                    }
                }
                if (u != "") {
                    B.val("");
                    var A = u.substring(u.length - 1);
                    if (A != ",") {
                        u = u + ","
                    }
                    M.val("," + u);
                    a("li.as-selection-item", G).addClass("blur").removeClass("selected")
                }
                B.after(M);
                G.click(function () {
                    F = true;
                    B.focus()
                }).mousedown(function () {
                    F = false
                }).after(o);
                var J = null;
                var y = null;
                var E = "";
                var q = 0;
                var r = false;
                var H = null;
                B.focus(function () {
                    if (!g.usePlaceholder && a(this).val() == g.startText && M.val() == "") {
                        a(this).val("")
                    } else {
                        if (F) {
                            a("li.as-selection-item", G).removeClass("blur");
                            if (a(this).val() != "") {
                                p.css("width", G.outerWidth());
                                o.show()
                            }
                        }
                    }
                    if (J) {
                        clearInterval(J)
                    }
                    J = setInterval(function () {
                        if (g.showResultList) {
                            if (g.selectionLimit && a("li.as-selection-item", G).length >= g.selectionLimit) {
                                p.html('<li class="as-message">' + g.limitText + "</li>");
                                o.show()
                            } else {
                                l()
                            }
                        }
                    }, g.keyDelay);
                    F = true;
                    if (g.minChars == 0) {
                        L(a(this).val())
                    }
                    return true
                }).blur(function () {
                    if (!g.usePlaceholder && a(this).val() == "" && M.val() == "" && u == "" && g.minChars > 0) {
                        a(this).val(g.startText)
                    } else {
                        if (F) {
                            a("li.as-selection-item", G).addClass("blur").removeClass("selected");
                            o.hide()
                        }
                    }
                    if (J) {
                        clearInterval(J)
                    }
                }).keydown(function (S) {
                    H = S.keyCode;
                    first_focus = false;
                    switch (S.keyCode) {
                        case 38:
                            S.preventDefault();
                            w("up");
                            break;
                        case 40:
                            S.preventDefault();
                            w("down");
                            break;
                        case 8:
                            if (B.val() == "") {
                                var O = M.val().split(",");
                                O = O[O.length - 2];
                                G.children().not(v.prev()).removeClass("selected");
                                if (v.prev().hasClass("selected")) {
                                    M.val(M.val().replace("," + O + ",", ","));
                                    g.selectionRemoved.call(this, v.prev())
                                } else {
                                    g.selectionClick.call(this, v.prev());
                                    v.prev().addClass("selected")
                                }
                            }
                            if (B.val().length == 1) {
                                o.hide();
                                E = "";
                                j()
                            }
                            if (a(":visible", o).length > 0) {
                                if (y) {
                                    clearTimeout(y)
                                }
                                y = setTimeout(function () {
                                    l()
                                }, g.keyDelay)
                            }
                            break;
                        case 9:
                        case 188:
                            if (g.canGenerateNewSelections) {
                                r = true;
                                var Q = B.val().replace(/(,)/g, "");
                                var R = a("li.active:first", o);
                                if (Q !== "" && M.val().search("," + Q + ",") < 0 && Q.length >= g.minChars && R.length === 0) {
                                    S.preventDefault();
                                    var P = {};
                                    P[g.selectedItemProp] = Q;
                                    P[g.selectedValuesProp] = Q;
                                    var x = a("li", G).length;
                                    K(P, "00" + (x + 1));
                                    B.val("");
                                    j();
                                    break
                                }
                            }
                            case 13:
                                r = false;
                                var R = a("li.active:first", o);
                                if (R.length > 0) {
                                    R.click();
                                    o.hide()
                                }
                                if (g.neverSubmit || R.length > 0) {
                                    S.preventDefault()
                                }
                                break;
                            case 27:
                            case 16:
                            case 20:
                                j();
                                o.hide();
                                break
                    }
                });

                function l() {
                    var x = B.val().replace(/[\\]+|[\/]+/g, "");
                    if (x == E) {
                        return
                    }
                    E = x;
                    if (x.length >= g.minChars) {
                        G.addClass("loading");
                        L(x)
                    } else {
                        G.removeClass("loading");
                        o.hide()
                    }
                }

                function L(x) {
                    if (g.beforeRetrieve) {
                        x = g.beforeRetrieve.call(this, x)
                    }
                    j();
                    b(x, s)
                }
                var t = 0;

                function s(Q, W) {
                    if (!g.matchCase) {
                        W = W.toLowerCase()
                    }
                    W = W.replace("(", "\\(", "g").replace(")", "\\)", "g");
                    var Y = 0;
                    o.html(p.html("")).hide();
                    var aa = d(Q);
                    for (var R = 0; R < aa; R++) {
                        var S = R;
                        t++;
                        var T = false;
                        if (g.searchObjProps == "value") {
                            var V = Q[S].value
                        } else {
                            var V = "";
                            var U = g.searchObjProps.split(",");
                            for (var X = 0; X < U.length; X++) {
                                var x = a.trim(U[X]);
                                V = V + Q[S][x] + " "
                            }
                        }
                        if (V) {
                            if (!g.matchCase) {
                                V = V.toLowerCase()
                            }
                            if (V.search(W) != -1 && M.val().search("," + Q[S][g.selectedValuesProp] + ",") == -1) {
                                T = true
                            }
                        }
                        if (T) {
                            var P = a('<li class="as-result-item" id="as-result-item-' + S + '"></li>').click(function () {
                                var ad = a(this).data("data");
                                var ab = ad.num;
                                if (a("#as-selection-" + ab, G).length <= 0 && !r) {
                                    var ac = ad.attributes;
                                    B.val("").focus();
                                    E = "";
                                    K(ac, ab);
                                    g.resultClick.call(this, ad);
                                    o.hide()
                                }
                                r = false
                            }).mousedown(function () {
                                F = false
                            }).mouseover(function () {
                                a("li", p).removeClass("active");
                                a(this).addClass("active")
                            }).data("data", {
                                attributes: Q[S],
                                num: t
                            });
                            var Z = a.extend({}, Q[S]);
                            if (!g.matchCase) {
                                var O = new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + W + ")(?![^<>]*>)(?![^&;]+;)", "gi")
                            } else {
                                var O = new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + W + ")(?![^<>]*>)(?![^&;]+;)", "g")
                            }
                            if (g.resultsHighlight && W.length > 0) {
                                Z[g.selectedItemProp] = Z[g.selectedItemProp].replace(O, "<em>$1</em>")
                            }
                            if (!g.formatList) {
                                P = P.html(Z[g.selectedItemProp])
                            } else {
                                P = g.formatList.call(this, Z, P)
                            }
                            p.append(P);
                            delete Z;
                            Y++;
                            if (g.retrieveLimit && g.retrieveLimit == Y) {
                                break
                            }
                        }
                    }
                    G.removeClass("loading");
                    if (Y <= 0) {
                        p.html('<li class="as-message">' + g.emptyText + "</li>")
                    }
                    p.css("width", G.outerWidth());
                    if (Y > 0 || !g.showResultListWhenNoMatch) {
                        o.show()
                    }
                    g.resultsComplete.call(this)
                }

                function K(P, x) {
                    M.val((M.val() || ",") + P[g.selectedValuesProp] + ",");
                    var O = a('<li class="as-selection-item" id="as-selection-' + x + '" data-value="' + P[g.selectedValuesProp] + '"></li>').click(function () {
                        g.selectionClick.call(this, a(this));
                        G.children().removeClass("selected");
                        a(this).addClass("selected")
                    }).mousedown(function () {
                        F = false
                    });
                    var Q = a('<a class="as-close">&times;</a>').click(function () {
                        M.val(M.val().replace("," + P[g.selectedValuesProp] + ",", ","));
                        g.selectionRemoved.call(this, O);
                        F = true;
                        B.focus();
                        return false
                    });
                    v.before(O.html(P[g.selectedItemProp]).prepend(Q));
                    g.selectionAdded.call(this, v.prev(), P[g.selectedValuesProp]);
                    return v.prev()
                }

                function w(P) {
                    if (a(":visible", o).length > 0) {
                        var x = a("li", o);
                        if (P == "down") {
                            var Q = x.eq(0)
                        } else {
                            var Q = x.filter(":last")
                        }
                        var O = a("li.active:first", o);
                        if (O.length > 0) {
                            if (P == "down") {
                                Q = O.next()
                            } else {
                                Q = O.prev()
                            }
                        }
                        x.removeClass("active");
                        Q.addClass("active")
                    }
                }

                function j() {
                    if (f) {
                        f.abort();
                        f = null
                    }
                }
            })
        }
    }
})(django.jQuery);