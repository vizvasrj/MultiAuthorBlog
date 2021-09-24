(function (a) {
    a.fn.autoSuggest = function (f, c) {
        var i = {
            asHtmlID: false,
            startText: "Enter Name Here",
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
        var e = a.extend(i, c);
        var d = "object";
        var h = 0;
        if (typeof f == "string") {
            d = "string";
            var b = f
        } else {
            var g = f;
            for (k in f) {
                if (f.hasOwnProperty(k)) {
                    h++
                }
            }
        }
        if ((d == "object" && h > 0) || d == "string") {
            return this.each(function (y) {
                if (!e.asHtmlID) {
                    y = y + "" + Math.floor(Math.random() * 100);
                    var l = "as-input-" + y
                } else {
                    y = e.asHtmlID;
                    var l = y
                }
                e.start.call(this);
                var A = a(this);
                A.attr("autocomplete", "off").addClass("as-input").attr("id", l).val(e.startText);
                var E = false;
                A.wrap('<ul class="as-selections" id="as-selections-' + y + '"></ul>').wrap('<li class="as-original" id="as-original-' + y + '"></li>');
                var F = a("#as-selections-" + y);
                var u = a("#as-original-" + y);
                var n = a('<div class="as-results" id="as-results-' + y + '"></div>').hide();
                var o = a('<ul class="as-list"></ul>');
                var I = a('<input type="hidden" class="as-values" name="as_values_' + y + '" id="as-values-' + y + '" />');
                var t = "";
                if (typeof e.preFill == "string") {
                    var B = e.preFill.split(",");
                    for (var G = 0; G < B.length; G++) {
                        var m = {};
                        m[e.selectedValuesProp] = B[G];
                        if (B[G] != "") {
                            H(m, "000" + G)
                        }
                    }
                    t = e.preFill
                } else {
                    t = "";
                    var J = 0;
                    for (k in e.preFill) {
                        if (e.preFill.hasOwnProperty(k)) {
                            J++
                        }
                    }
                    if (J > 0) {
                        for (var G = 0; G < J; G++) {
                            var C = e.preFill[G][e.selectedValuesProp];
                            if (C == undefined) {
                                C = ""
                            }
                            t = t + C + ",";
                            if (C != "") {
                                H(e.preFill[G], "000" + G)
                            }
                        }
                    }
                }
                if (t != "") {
                    A.val("");
                    var z = t.substring(t.length - 1);
                    if (z != ",") {
                        t = t + ","
                    }
                    I.val("," + t);
                    a("li.as-selection-item", F).addClass("blur").removeClass("selected")
                }
                A.after(I);
                F.click(function () {
                    E = true;
                    A.focus()
                }).mousedown(function () {
                    E = false
                }).after(n);
                var w = null;
                var D = "";
                var p = 0;
                var q = false;
                A.focus(function () {
                    if (a(this).val() == e.startText && I.val() == "") {
                        a(this).val("")
                    } else {
                        if (E) {
                            a("li.as-selection-item", F).removeClass("blur");
                            if (a(this).val() != "") {
                                o.css("width", F.outerWidth());
                                n.show()
                            }
                        }
                    }
                    E = true;
                    return true
                }).blur(function (M) {
                    if (a(this).val() == "" && I.val() == "" && t == "") {
                        a(this).val(e.startText)
                    } else {
                        if (E) {
                            a("li.as-selection-item", F).addClass("blur").removeClass("selected");
                            n.hide()
                        }
                    }
                    if (a(this).val() != "" && a(this).val().match(/.+@.+\..+/)) {
                        q = true;
                        var L = A.val().replace(/(,)/g, "");
                        if (L != "" && I.val().search("," + L + ",") < 0 && L.length >= e.minChars) {
                            M.preventDefault();
                            var K = {};
                            K[e.selectedItemProp] = L;
                            K[e.selectedValuesProp] = L;
                            var x = a("li", F).length;
                            H(K, "00" + (x + 1));
                            A.val("")
                        }
                    }
                }).keydown(function (O) {
                    lastKeyPressCode = O.keyCode;
                    first_focus = false;
                    switch (O.keyCode) {
                        case 38:
                            O.preventDefault();
                            v("up");
                            break;
                        case 40:
                            O.preventDefault();
                            v("down");
                            break;
                        case 8:
                            if (A.val() == "") {
                                var K = I.val().split(",");
                                K = K[K.length - 2];
                                F.children().not(u.prev()).removeClass("selected");
                                if (u.prev().hasClass("selected")) {
                                    I.val(I.val().replace("," + K + ",", ","));
                                    e.selectionRemoved.call(this, u.prev())
                                } else {
                                    e.selectionClick.call(this, u.prev());
                                    u.prev().addClass("selected")
                                }
                            }
                            if (A.val().length == 1) {
                                n.hide();
                                D = ""
                            }
                            if (a(":visible", n).length > 0) {
                                if (w) {
                                    clearTimeout(w)
                                }
                                w = setTimeout(function () {
                                    j()
                                }, e.keyDelay)
                            }
                            break;
                        case 9:
                        case 188:
                            q = true;
                            var M = A.val().replace(/(,)/g, "");
                            if (M != "" && I.val().search("," + M + ",") < 0 && M.length >= e.minChars) {
                                O.preventDefault();
                                var L = {};
                                L[e.selectedItemProp] = M;
                                L[e.selectedValuesProp] = M;
                                var x = a("li", F).length;
                                H(L, "00" + (x + 1));
                                A.val("")
                            } else {
                                if (O.keyCode == 9) {
                                    if (O.target.id == "send_to") {
                                        a("#send_to_cc").focus()
                                    } else {
                                        if (O.target.id == "send_to_cc") {
                                            a("#send_to_bcc").focus()
                                        } else {
                                            if (O.target.id == "send_to_bcc") {
                                                a("input[name=subject]")[0].focus()
                                            }
                                        }
                                    }
                                }
                            }
                            case 13:
                                q = false;
                                var N = a("li.active:first", n);
                                if (N.length > 0) {
                                    N.click();
                                    n.hide()
                                }
                                if (e.neverSubmit || N.length > 0) {
                                    O.preventDefault()
                                }
                                break;
                            default:
                                if (e.showResultList) {
                                    if (e.selectionLimit && a("li.as-selection-item", F).length >= e.selectionLimit) {
                                        o.html('<li class="as-message">' + e.limitText + "</li>");
                                        n.show()
                                    } else {
                                        if (w) {
                                            clearTimeout(w)
                                        }
                                        w = setTimeout(function () {
                                            j()
                                        }, e.keyDelay)
                                    }
                                }
                                break
                    }
                });

                function j() {
                    if (lastKeyPressCode == 46 || (lastKeyPressCode > 8 && lastKeyPressCode < 32)) {
                        return n.hide()
                    }
                    var K = A.val().replace(/[\\]+|[\/]+/g, "");
                    if (K == D) {
                        return
                    }
                    D = K;
                    if (K.length >= e.minChars) {
                        F.addClass("loading");
                        if (d == "string") {
                            var x = "";
                            if (e.retrieveLimit) {
                                x = "&limit=" + encodeURIComponent(e.retrieveLimit)
                            }
                            if (e.beforeRetrieve) {
                                K = e.beforeRetrieve.call(this, K)
                            }
                            a.getJSON(b + "?" + e.queryParam + "=" + encodeURIComponent(K) + x + e.extraParams, function (M) {
                                h = 0;
                                var L = e.retrieveComplete.call(this, M);
                                for (k in L) {
                                    if (L.hasOwnProperty(k)) {
                                        h++
                                    }
                                }
                                r(L, K)
                            })
                        } else {
                            if (e.beforeRetrieve) {
                                K = e.beforeRetrieve.call(this, K)
                            }
                            r(g, K)
                        }
                    } else {
                        F.removeClass("loading");
                        n.hide()
                    }
                }
                var s = 0;

                function r(M, S) {
                    if (!e.matchCase) {
                        S = S.toLowerCase()
                    }
                    var U = 0;
                    n.html(o.html("")).hide();
                    for (var N = 0; N < h; N++) {
                        var O = N;
                        s++;
                        var P = false;
                        if (e.searchObjProps == "value") {
                            var Q = M[O].value
                        } else {
                            var Q = "";
                            var R = e.searchObjProps.split(",");
                            for (var T = 0; T < R.length; T++) {
                                var x = a.trim(R[T]);
                                Q = Q + M[O][x] + " "
                            }
                        }
                        if (Q) {
                            if (!e.matchCase) {
                                Q = Q.toLowerCase()
                            }
                            if (Q.search(S) != -1 && I.val().search("," + M[O][e.selectedValuesProp] + ",") == -1) {
                                P = true
                            }
                        }
                        if (P) {
                            var L = a('<li class="as-result-item" id="as-result-item-' + O + '"></li>').click(function () {
                                var Y = a(this).data("data");
                                var W = Y.num;
                                if (a("#as-selection-" + W, F).length <= 0 && !q) {
                                    var X = Y.attributes;
                                    A.val("").focus();
                                    D = "";
                                    H(X, W);
                                    e.resultClick.call(this, Y);
                                    n.hide()
                                }
                                q = false
                            }).mousedown(function () {
                                E = false
                            }).mouseover(function () {
                                a("li", o).removeClass("active");
                                a(this).addClass("active")
                            }).data("data", {
                                attributes: M[O],
                                num: s
                            });
                            var V = a.extend({}, M[O]);
                            if (!e.matchCase) {
                                var K = new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + S + ")(?![^<>]*>)(?![^&;]+;)", "gi")
                            } else {
                                var K = new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + S + ")(?![^<>]*>)(?![^&;]+;)", "g")
                            }
                            if (e.resultsHighlight) {
                                V[e.selectedItemProp] = V[e.selectedItemProp].replace(K, "<em>$1</em>")
                            }
                            if (!e.formatList) {
                                L = L.html(V[e.selectedItemProp])
                            } else {
                                L = e.formatList.call(this, V, L)
                            }
                            o.append(L);
                            delete V;
                            U++;
                            if (e.retrieveLimit && e.retrieveLimit == U) {
                                break
                            }
                        }
                    }
                    F.removeClass("loading");
                    if (U <= 0) {
                        o.html('<li class="as-message">' + e.emptyText + "</li>")
                    }
                    o.css("width", F.outerWidth());
                    n.show();
                    e.resultsComplete.call(this)
                }

                function H(M, x) {
                    I.val(I.val() + M[e.selectedValuesProp] + ",");
                    var K = a('<li class="as-selection-item" id="as-selection-' + x + '"></li>').click(function () {
                        e.selectionClick.call(this, a(this));
                        F.children().removeClass("selected");
                        a(this).addClass("selected")
                    }).mousedown(function () {
                        E = false
                    });
                    var N = a('<a class="as-close">&times;</a>').click(function () {
                        I.val(I.val().replace("," + M[e.selectedValuesProp] + ",", ","));
                        e.selectionRemoved.call(this, K);
                        E = true;
                        A.focus();
                        return false
                    });
                    var L = M[e.selectedItemProp] ? M[e.selectedItemProp] : M.value;
                    u.before(K.html(L).prepend(N));
                    e.selectionAdded.call(this, u.prev())
                }

                function v(L) {
                    if (a(":visible", n).length > 0) {
                        var x = a("li", n);
                        if (L == "down") {
                            var M = x.eq(0)
                        } else {
                            var M = x.filter(":last")
                        }
                        var K = a("li.active:first", n);
                        if (K.length > 0) {
                            if (L == "down") {
                                M = K.next()
                            } else {
                                M = K.prev()
                            }
                        }
                        x.removeClass("active");
                        M.addClass("active")
                    }
                }
            })
        }
    }
})(jQuery);