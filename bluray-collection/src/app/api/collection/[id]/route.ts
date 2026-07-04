import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { isFormat } from "@/lib/formats";

export const dynamic = "force-dynamic";

function parseId(param: string): number | null {
  const id = Number(param);
  return Number.isInteger(id) ? id : null;
}

// PATCH /api/collection/:id → modifie le format ou les notes
export async function PATCH(req: NextRequest, { params }: { params: { id: string } }) {
  const id = parseId(params.id);
  if (id == null) return NextResponse.json({ error: "id invalide" }, { status: 400 });

  let body: any;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const data: { format?: string; notes?: string | null } = {};
  if (body?.format !== undefined) {
    if (!isFormat(body.format)) {
      return NextResponse.json({ error: "Format invalide" }, { status: 400 });
    }
    data.format = body.format;
  }
  if (body?.notes !== undefined) {
    data.notes = typeof body.notes === "string" ? body.notes.trim() || null : null;
  }

  try {
    const item = await prisma.bluRay.update({ where: { id }, data });
    return NextResponse.json({ item });
  } catch {
    return NextResponse.json({ error: "Introuvable" }, { status: 404 });
  }
}

// DELETE /api/collection/:id → retire un film de la collection
export async function DELETE(_req: NextRequest, { params }: { params: { id: string } }) {
  const id = parseId(params.id);
  if (id == null) return NextResponse.json({ error: "id invalide" }, { status: 400 });

  try {
    await prisma.bluRay.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ error: "Introuvable" }, { status: 404 });
  }
}
